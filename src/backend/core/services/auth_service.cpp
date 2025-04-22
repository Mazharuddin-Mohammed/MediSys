#include "auth_service.h"
#include "../models/user.h"
#include <bcrypt/BCrypt.hpp>

AuthService::AuthService(std::shared_ptr<DBManager> db) : db_manager(db) {
    auto& conn = db_manager->getConnection();
    conn.prepare("select_user", "SELECT id, password_hash FROM users WHERE username = $1");
    conn.prepare("log_audit",
        "SELECT log_audit_action($1, $2, $3, $4, $5, $6, $7)");
}

int AuthService::authenticate(const std::string& username, const std::string& password) {
    if (!UserModel::isValidUsername(username)) {
        throw std::invalid_argument("Invalid username");
    }

    pqxx::work txn(db_manager->getConnection());
    auto result = txn.exec_prepared("select_user", username);
    if (result.empty()) {
        txn.exec_prepared("log_audit",
            0, "failed_login", "user", 0,
            pqxx::to_json({{"username", username}, {"reason", "user not found"}}),
            "unknown", "unknown");
        throw std::runtime_error("Invalid credentials");
    }

    auto row = result[0];
    int user_id = row[0].as<int>();
    std::string stored_hash = row[1].as<std::string>();

    if (!verifyPassword(password, stored_hash)) {
        txn.exec_prepared("log_audit",
            0, "failed_login", "user", user_id,
            pqxx::to_json({{"username", username}, {"reason", "incorrect password"}}),
            "unknown", "unknown");
        throw std::runtime_error("Invalid credentials");
    }

    txn.exec_prepared("log_audit",
        user_id, "successful_login", "user", user_id,
        pqxx::to_json({{"username", username}}),
        "unknown", "unknown");
    txn.commit();
    return user_id;
}

std::string AuthService::hashPassword(const std::string& password) const {
    return BCrypt::generateHash(password);
}

bool AuthService::verifyPassword(const std::string& password, const std::string& hash) const {
    return BCrypt::validatePassword(password, hash);
}