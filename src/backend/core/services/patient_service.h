#pragma once
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