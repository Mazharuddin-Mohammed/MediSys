#include "patient_service.h"
#include "../models/patient.h"
#include <sstream>
#include <iomanip>

PatientService::PatientService(std::shared_ptr<DBManager> db) : db_manager(db) {
    auto& conn = db_manager->getConnection();
    conn.prepare("insert_patient",
        "INSERT INTO patients (first_name, last_name, dob, gender, address, mobile, email, "
        "emergency_contact_name, emergency_contact_mobile) "
        "VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9) RETURNING id");
    conn.prepare("select_patient",
        "SELECT id, first_name, last_name, dob, gender, address, mobile, email, "
        "emergency_contact_name, emergency_contact_mobile "
        "FROM patients WHERE id = $1");
}

int PatientService::createPatient(const Patient& patient, int user_id, const std::string& ip, const std::string& session) {
    if (!PatientModel::isValidName(patient.first_name) || !PatientModel::isValidName(patient.last_name)) {
        throw std::invalid_argument("Invalid name");
    }
    if (!PatientModel::isValidGender(patient.gender)) {
        throw std::invalid_argument("Invalid gender");
    }
    if (!PatientModel::isValidMobile(patient.mobile)) {
        throw std::invalid_argument("Invalid mobile");
    }
    if (!PatientModel::isValidEmail(patient.email)) {
        throw std::invalid_argument("Invalid email");
    }

    db_manager->setAuditContext(user_id, ip, session);
    pqxx::work txn(db_manager->getConnection());
    // Convert time_t to formatted date string
    std::tm* tm_ptr = std::localtime(&patient.dob);
    char date_buffer[11]; // YYYY-MM-DD + null terminator
    std::strftime(date_buffer, sizeof(date_buffer), "%Y-%m-%d", tm_ptr);

    auto result = txn.exec_prepared("insert_patient",
        patient.first_name,
        patient.last_name,
        std::string(date_buffer), // Formatted date string
        patient.gender,
        patient.address,
        patient.mobile,
        patient.email,
        patient.emergency_contact_name,
        patient.emergency_contact_mobile
    );
    txn.commit();
    return result[0][0].as<int>();
}

Patient PatientService::getPatient(int patient_id, int user_id, const std::string& ip, const std::string& session) {
    if (patient_id <= 0) {
        throw std::invalid_argument("Invalid patient ID");
    }

    db_manager->setAuditContext(user_id, ip, session);
    pqxx::work txn(db_manager->getConnection());
    auto result = txn.exec_prepared("select_patient", patient_id);
    if (result.empty()) {
        throw std::runtime_error("Patient not found");
    }

    auto row = result[0];
    Patient patient;
    patient.id = row[0].as<int>();
    patient.first_name = row[1].as<std::string>();
    patient.last_name = row[2].as<std::string>();
    // Convert date string to time_t
    std::tm tm = {};
    std::string date_str = row[3].as<std::string>();
    std::stringstream ss(date_str);
    ss >> std::get_time(&tm, "%Y-%m-%d");
    patient.dob = std::mktime(&tm);
    patient.gender = row[4].as<std::string>();
    patient.address = row[5].as<std::string>();
    patient.mobile = row[6].as<std::string>();
    patient.email = row[7].as<std::string>();
    patient.emergency_contact_name = row[8].as<std::string>();
    patient.emergency_contact_mobile = row[9].as<std::string>();
    return patient;
}