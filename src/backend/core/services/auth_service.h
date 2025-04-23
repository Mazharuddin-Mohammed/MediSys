#pragma once

/**
 * MediSys Hospital Management System - Authentication Service Header
 *
 * This file defines the AuthService class which handles user authentication,
 * password hashing, and verification. It provides a secure interface for
 * validating user credentials against the database.
 *
 * Author: Mazharuddin Mohammed
 */

#include "../database/db_manager.h"
#include <memory>
#include <string>

class AuthService {
public:
    AuthService(std::shared_ptr<DBManager> db);
    int authenticate(const std::string& username, const std::string& password);

private:
    std::shared_ptr<DBManager> db_manager;
    std::string hashPassword(const std::string& password) const;
    bool verifyPassword(const std::string& password, const std::string& hash) const;
};