#include "patient.h"
#include <regex>

bool PatientModel::isValidName(const std::string& name) {
    return !name.empty() && name.length() <= 50 &&
           std::all_of(name.begin(), name.end(), [](char c) {
               return std::isalpha(c) || c == ' ' || c == '-';
           });
}

bool PatientModel::isValidGender(const std::string& gender) {
    return gender == "male" || gender == "female" || gender == "other";
}

bool PatientModel::isValidMobile(const std::string& mobile) {
    if (mobile.empty()) return true; // Mobile is optional
    return mobile.length() <= 15 && std::regex_match(mobile, std::regex("^\\+?[0-9]{7,15}$"));
}

bool PatientModel::isValidEmail(const std::string& email) {
    if (email.empty()) return true; // Email is optional
    return email.length() <= 100 &&
           std::regex_match(email, std::regex("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"));
}