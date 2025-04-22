#include <pybind11/pybind11.h>
#include "db_manager.h"
#include "auth_service.h"

namespace py = pybind11;

PYBIND11_MODULE(medisys_bindings, m) {
    py::class_<DBManager>(m, "DBManager")
        .def(py::init<const std::string&>())
        .def("initialize_schema", &DBManager::initializeSchema)
        .def("set_audit_context", &DBManager::setAuditContext, py::arg("user_id"), py::arg("ip_address"), py::arg("session_id"));

    py::class_<AuthService>(m, "AuthService")
        .def(py::init<std::shared_ptr<DBManager>>())
        .def("authenticate", [](AuthService& self, const std::string& username, const std::string& password) {
            if (username.empty() || password.empty()) {
                throw py::value_error("Username and password cannot be empty");
            }
            try {
                return self.authenticate(username, password);
            } catch (const std::exception& e) {
                throw py::runtime_error("Authentication failed");
            }
        });
}