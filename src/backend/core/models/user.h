#pragma once

/**
 * MediSys Hospital Management System - User Model
 *
 * This file defines the User structure and UserModel class which represent
 * user data and provide validation methods for user attributes. The User
 * structure contains authentication and role information for system users.
 *
 * Author: Mazharuddin Mohammed
 */

#include <string>

struct User {
    int id;
    std::string username;
    std::string password_hash;
    std::string role; // admin, finance, doctor, department_head, administration
    std::string first_name;
    std::string last_name;
    std::string email;
    bool mfa_enabled;
};

class UserModel {
public:
    static bool isValidUsername(const std::string& username);
    static bool isValidRole(const std::string& role);
    static bool isValidEmail(const std::string& email);
};