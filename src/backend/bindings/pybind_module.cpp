/**
 * MediSys Hospital Management System - Python Bindings Module
 *
 * This file implements the Python bindings for the MediSys C++ backend using pybind11.
 * It exposes core functionality like database management, authentication, and patient
 * services to the Python frontend, allowing seamless integration between components.
 *
 * Author: Mazharuddin Mohammed
 */

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "../core/database/db_manager.h"
#include "../core/services/auth_service.h"
#include "../core/services/patient_service.h"
#include "../core/models/patient.h"

namespace py = pybind11;

PYBIND11_MODULE(medisys_bindings, m) {
    py::class_<DBManager, std::shared_ptr<DBManager>>(m, "DBManager")
        .def(py::init<const std::string&>())
        .def("initialize_schema", &DBManager::initializeSchema)
        .def("set_audit_context", &DBManager::setAuditContext, py::arg("user_id"), py::arg("ip_address"), py::arg("session_id"))
        .def("get_connection", [](DBManager& self) -> pqxx::connection& { return self.getConnection(); },
             py::return_value_policy::reference);

    py::class_<AuthService, std::shared_ptr<AuthService>>(m, "AuthService")
        .def(py::init<std::shared_ptr<DBManager>>())
        .def("authenticate", [](AuthService& self, const std::string& username, const std::string& password) {
            if (username.empty() || password.empty()) {
                throw py::value_error("Username and password cannot be empty");
            }
            try {
                return self.authenticate(username, password);
            } catch (const std::exception& e) {
                throw py::value_error(std::string("Authentication failed: ") + e.what());
                return -1; // This line will never be reached
            }
        });

    py::class_<Patient>(m, "Patient")
        .def(py::init<>())
        .def_readwrite("id", &Patient::id)
        .def_readwrite("first_name", &Patient::first_name)
        .def_readwrite("last_name", &Patient::last_name)
        .def_readwrite("dob", &Patient::dob)
        .def_readwrite("gender", &Patient::gender)
        .def_readwrite("address", &Patient::address)
        .def_readwrite("mobile", &Patient::mobile)
        .def_readwrite("email", &Patient::email)
        .def_readwrite("emergency_contact_name", &Patient::emergency_contact_name)
        .def_readwrite("emergency_contact_mobile", &Patient::emergency_contact_mobile);

    py::class_<PatientService, std::shared_ptr<PatientService>>(m, "PatientService")
        .def(py::init<std::shared_ptr<DBManager>>())
        .def("create_patient", &PatientService::createPatient,
             py::arg("patient"), py::arg("user_id"), py::arg("ip"), py::arg("session"))
        .def("get_patient", &PatientService::getPatient,
             py::arg("patient_id"), py::arg("user_id"), py::arg("ip"), py::arg("session"));
}