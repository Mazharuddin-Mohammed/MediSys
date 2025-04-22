#include "db_manager.h"
#include <fstream>
#include <sstream>

DBManager::DBManager(const std::string& conn_str) {
    conn = std::make_unique<pqxx::connection>(conn_str + " sslmode=verify-full");
    if (!conn->is_open()) {
        throw std::runtime_error("Failed to connect to database");
    }
    conn->prepare("set_user_context", "SET medisys.user_id = $1, medisys.ip_address = $2, medisys.session_id = $3");
    conn->prepare("insert_patient",
        "INSERT INTO patients (first_name, last_name, dob, address) VALUES ($1, $2, $3, $4) RETURNING id");
    conn->prepare("log_audit",
        "SELECT log_audit_action($1, $2, $3, $4, $5, $6, $7)");
}

DBManager::~DBManager() {
    conn->close();
}

void DBManager::initializeSchema() {
    std::ifstream schema_file("src/backend/core/database/schema.sql");
    if (!schema_file.is_open()) {
        throw std::runtime_error("Failed to open schema file");
    }
    std::stringstream buffer;
    buffer << schema_file.rdbuf();
    pqxx::work txn(*conn);
    txn.exec(buffer.str());
    txn.commit();
}

void DBManager::setAuditContext(int user_id, const std::string& ip_address, const std::string& session_id) {
    pqxx::work txn(*conn);
    txn.exec_prepared("set_user_context", user_id, ip_address, session_id);
    txn.commit();
}