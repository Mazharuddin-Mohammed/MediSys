#pragma once
#include <string>

struct Doctor {
    int id;
    int user_id;
    int department_id;
    std::string first_name;
    std::string last_name;
    std::string specialization;
    std::string license_number;
    std::string mobile;
};

class DoctorModel {
public:
    static bool isValidName(const std::string& name);
    static bool isValidSpecialization(const std::string& specialization);
    static bool isValidLicenseNumber(const std::string& license_number);
    static bool isValidMobile(const std::string& mobile);
};