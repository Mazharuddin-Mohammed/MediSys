#pragma once
#include <string>
#include <ctime>

struct Patient {
    int id;
    std::string first_name;
    std::string last_name;
    std::time_t dob; // Stored as UNIX timestamp
    std::string gender;
    std::string address;
    std::string mobile;
    std::string email;
    std::string emergency_contact_name;
    std::string emergency_contact_mobile;
};

class PatientModel {
public:
    static bool isValidName(const std::string& name);
    static bool isValidGender(const std::string& gender);
    static bool isValidMobile(const std::string& mobile);
    static bool isValidEmail(const std::string& email);
};