#include "user.h"
#include <regex>

bool UserModel::isValidUsername(const std::string& username) {
    return !username.empty() && username.length() <= 50 &&
           std::regex_match(username, std::regex("^[a-zA-Z0-9_]+$"));
}

bool UserModel::isValidRole(const std::string& role) {
    return role == "admin" || role == "finance" || role == "doctor" ||
           role == "department_head" || role == "administration";
}

bool UserModel::isValidEmail(const std::string& email) {
    if (email.empty()) return true; // Email is optional
    return email.length() <= 100 &&
           std::regex_match(email, std::regex("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"));
}