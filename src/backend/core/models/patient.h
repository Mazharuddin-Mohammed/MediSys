#pragma once

/**
 * MediSys Hospital Management System - Patient Model
 *
 * This file defines the Patient structure and PatientModel class which represent
 * patient data and provide validation methods for patient attributes. The Patient
 * structure contains all relevant patient information used throughout the system.
 *
 * Author: Mazharuddin Mohammed
 */

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