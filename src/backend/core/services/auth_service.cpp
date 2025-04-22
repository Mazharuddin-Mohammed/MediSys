#include "auth_service.h"
#include "../models/user.h"
#include <iomanip>
#include <sstream>
#include <openssl/sha.h>

AuthService::AuthService(std::shared_ptr<DBManager> db) : db_manager(db) {
    // Use the DBManager's safelyPrepare method to avoid duplicate prepared statements
    db_manager->safelyPrepare("select_user", "SELECT id, password_hash FROM users WHERE username = $1");
    db_manager->safelyPrepare("log_audit", "SELECT log_audit_action($1, $2, $3, $4, $5, $6, $7)");
}

int AuthService::authenticate(const std::string& username, const std::string& password) {
    if (!UserModel::isValidUsername(username)) {
        throw std::invalid_argument("Invalid username");
    }

    pqxx::work txn(db_manager->getConnection());
    auto result = txn.exec_prepared("select_user", username);
    if (result.empty()) {
        std::string json = "{\"username\":\"" + username + "\", \"reason\":\"user not found\"}";
        txn.exec_prepared("log_audit",
            0, "failed_login", "user", 0,
            json,
            "unknown", "unknown");
        throw std::runtime_error("Invalid credentials");
    }

    auto row = result[0];
    int user_id = row[0].as<int>();
    std::string stored_hash = row[1].as<std::string>();

    if (!verifyPassword(password, stored_hash)) {
        std::string json = "{\"username\":\"" + username + "\", \"reason\":\"incorrect password\"}";
        txn.exec_prepared("log_audit",
            0, "failed_login", "user", user_id,
            json,
            "unknown", "unknown");
        throw std::runtime_error("Invalid credentials");
    }

    std::string json = "{\"username\":\"" + username + "\"}";
    txn.exec_prepared("log_audit",
        user_id, "successful_login", "user", user_id,
        json,
        "unknown", "unknown");
    txn.commit();
    return user_id;
}

std::string AuthService::hashPassword(const std::string& password) const {
    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256_CTX sha256;
    SHA256_Init(&sha256);
    SHA256_Update(&sha256, password.c_str(), password.size());
    SHA256_Final(hash, &sha256);

    std::stringstream ss;
    for(int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
        ss << std::hex << std::setw(2) << std::setfill('0') << (int)hash[i];
    }
    return ss.str();
}

bool AuthService::verifyPassword(const std::string& password, const std::string& hash) const {
    return hashPassword(password) == hash;
}