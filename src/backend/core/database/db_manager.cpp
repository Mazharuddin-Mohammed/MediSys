/**
 * MediSys Hospital Management System - Database Manager Implementation
 *
 * This file implements the DBManager class which handles database connections,
 * schema initialization, and provides a common interface for database operations.
 * It includes methods for setting up the database schema, preparing statements,
 * and managing audit context for tracking user actions.
 *
 * Author: Mazharuddin Mohammed
 */

#include "db_manager.h"
#include <fstream>
#include <sstream>

DBManager::DBManager(const std::string& conn_str) {
    conn = std::make_unique<pqxx::connection>(conn_str + " sslmode=disable");
    if (!conn->is_open()) {
        throw std::runtime_error("Failed to connect to database");
    }
    // Create the custom variables if they don't exist
    pqxx::work txn(*conn);
    txn.exec("DO $$\n"
           "BEGIN\n"
           "    IF NOT EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = 'medisys') THEN\n"
           "        CREATE SCHEMA medisys;\n"
           "    END IF;\n"
           "END\n"
           "$$;");
    txn.exec("DO $$\n"
           "BEGIN\n"
           "    IF NOT EXISTS (SELECT 1 FROM pg_settings WHERE name = 'medisys.user_id') THEN\n"
           "        PERFORM set_config('medisys.user_id', '0', false);\n"
           "    END IF;\n"
           "    IF NOT EXISTS (SELECT 1 FROM pg_settings WHERE name = 'medisys.ip_address') THEN\n"
           "        PERFORM set_config('medisys.ip_address', 'unknown', false);\n"
           "    END IF;\n"
           "    IF NOT EXISTS (SELECT 1 FROM pg_settings WHERE name = 'medisys.session_id') THEN\n"
           "        PERFORM set_config('medisys.session_id', 'unknown', false);\n"
           "    END IF;\n"
           "END\n"
           "$$;");
    txn.commit();

    // Prepare statements
    safelyPrepare("set_user_context", "SELECT set_config('medisys.user_id', $1::text, false), "
                                    "set_config('medisys.ip_address', $2, false), "
                                    "set_config('medisys.session_id', $3, false)");
    safelyPrepare("insert_patient",
        "INSERT INTO patients (first_name, last_name, dob, address) VALUES ($1, $2, $3, $4) RETURNING id");
    safelyPrepare("log_audit",
        "SELECT log_audit_action($1, $2, $3, $4, $5, $6, $7)");
}

DBManager::~DBManager() {
    conn->close();
}

void DBManager::initializeSchema() {
    // Check if the schema already exists
    pqxx::work check_txn(*conn);
    auto result = check_txn.exec("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'users')");
    bool schema_exists = result[0][0].as<bool>();
    check_txn.commit();

    if (!schema_exists) {
        std::ifstream schema_file("src/backend/core/database/schema.sql");
        if (!schema_file.is_open()) {
            throw std::runtime_error("Failed to open schema file");
        }
        std::stringstream buffer;
        buffer << schema_file.rdbuf();
        pqxx::work txn(*conn);
        txn.exec(buffer.str());

        // Create default admin user with password 'admin'
        // SHA-256 hash of 'admin' is 8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918
        txn.exec("INSERT INTO users (username, password_hash, email, role, created_at) "
                "VALUES ('admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', "
                "'admin@medisys.com', 'admin', CURRENT_TIMESTAMP) "
                "ON CONFLICT (username) DO NOTHING");

        txn.commit();
        std::cout << "Database schema initialized successfully" << std::endl;
        std::cout << "Default admin user created with username 'admin' and password 'admin'" << std::endl;
    } else {
        std::cout << "Database schema already exists, skipping initialization" << std::endl;

        // Check if admin user exists, create if not
        pqxx::work txn(*conn);
        auto result = txn.exec("SELECT COUNT(*) FROM users WHERE username = 'admin'");
        bool admin_exists = result[0][0].as<int>() > 0;

        if (!admin_exists) {
            // Create default admin user with password 'admin'
            // SHA-256 hash of 'admin' is 8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918
            txn.exec("INSERT INTO users (username, password_hash, email, role, created_at) "
                    "VALUES ('admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', "
                    "'admin@medisys.com', 'admin', CURRENT_TIMESTAMP)");
            txn.commit();
            std::cout << "Default admin user created with username 'admin' and password 'admin'" << std::endl;
        } else {
            txn.commit();
        }
    }
}

void DBManager::setAuditContext(int user_id, const std::string& ip_address, const std::string& session_id) {
    pqxx::work txn(*conn);
    txn.exec_prepared("set_user_context", std::to_string(user_id), ip_address, session_id);
    txn.commit();
}

bool DBManager::preparedStatementExists(const std::string& name) {
    try {
        pqxx::work txn(*conn);
        auto result = txn.exec("SELECT COUNT(*) FROM pg_prepared_statements WHERE name = '" + name + "'");
        txn.commit();
        return result[0][0].as<int>() > 0;
    } catch (const std::exception& e) {
        // If there's an error, assume the statement doesn't exist
        std::cerr << "Error checking for prepared statement: " << e.what() << std::endl;
        return false;
    }
}

void DBManager::safelyPrepare(const std::string& name, const std::string& query) {
    if (!preparedStatementExists(name)) {
        try {
            conn->prepare(name, query);
        } catch (const std::exception& e) {
            std::cerr << "Error preparing statement '" << name << "': " << e.what() << std::endl;
            // If the error is that the statement already exists, we can ignore it
            if (std::string(e.what()).find("already exists") == std::string::npos) {
                throw; // Re-throw if it's not an 'already exists' error
            }
        }
    }
}