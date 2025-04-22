#include "doctor.h"
#include <regex>

bool DoctorModel::isValidName(const std::string& name) {
    return !name.empty() && name.length() <= 50 &&
           std::all_of(name.begin(), name.end(), [](char c) {
               return std::isalpha(c) || c == ' ' || c == '-';
           });
}

bool DoctorModel::isValidSpecialization(const std::string& specialization) {
    return specialization.empty() || specialization.length() <= 100;
}

bool DoctorModel::isValidLicenseNumber(const std::string& license_number) {
    return license_number.empty() || (license_number.length() <= 50 &&
           std::regex_match(license_number, std::regex("^[A-Z0-9-]+$")));
}

bool DoctorModel::isValidMobile(const std::string& mobile) {
    if (mobile.empty()) return true; // Mobile is optional
    return mobile.length() <= 15 && std::regex_match(mobile, std::regex("^\\+?[0-9]{7,15}$"));
}