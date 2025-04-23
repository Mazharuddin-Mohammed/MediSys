#pragma once

/**
 * MediSys Hospital Management System - Patient Service Header
 *
 * This file defines the PatientService class which handles patient-related
 * operations such as creating, retrieving, and updating patient records.
 * It provides a secure interface for managing patient data with audit logging.
 *
 * Author: Mazharuddin Mohammed
 */

#include "../database/db_manager.h"
#include "../models/patient.h"
#include <memory>
#include <string>

class PatientService {
public:
    PatientService(std::shared_ptr<DBManager> db);
    int createPatient(const Patient& patient, int user_id, const std::string& ip, const std::string& session);
    Patient getPatient(int patient_id, int user_id, const std::string& ip, const std::string& session);

private:
    std::shared_ptr<DBManager> db_manager;
};