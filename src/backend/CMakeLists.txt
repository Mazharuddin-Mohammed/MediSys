set(BACKEND_SOURCES
    core/models/user.cpp
    core/models/patient.cpp
    core/models/doctor.cpp
    core/models/department.cpp
)

if(USE_POSTGRES)
    list(APPEND BACKEND_SOURCES
        core/database/db_manager.cpp
        core/services/auth_service.cpp
        core/services/patient_service.cpp
    )
else()
    # Add mock implementations for database-dependent components
    file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/mock_db_manager.cpp "
        #include \"../../src/backend/core/database/db_manager.h\"
        #include <iostream>
        // Implementation of DBManager methods
        DBManager::DBManager(const std::string& conn_str) {
            std::cout << \"Mock DBManager created with connection string: \" << conn_str << std::endl;
        }

        DBManager::~DBManager() {
            std::cout << \"Mock DBManager destroyed\" << std::endl;
        }

        void DBManager::initializeSchema() {
            std::cout << \"Mock schema initialization\" << std::endl;
        }

        void DBManager::setAuditContext(int user_id, const std::string& ip_address, const std::string& session_id) {
            std::cout << \"Mock audit context set for user \" << user_id << std::endl;
        }
    ")
    list(APPEND BACKEND_SOURCES ${CMAKE_CURRENT_BINARY_DIR}/mock_db_manager.cpp)

    file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/mock_auth_service.cpp "
        #include \"../../src/backend/core/services/auth_service.h\"
        #include <iostream>
        AuthService::AuthService(std::shared_ptr<DBManager> db) : db_manager(db) {
            std::cout << \"Mock AuthService created\" << std::endl;
        }
        int AuthService::authenticate(const std::string& username, const std::string& password) {
            std::cout << \"Mock authentication for user: \" << username << std::endl;
            if (username == \"admin\" && password == \"admin\") {
                return 1; // Mock admin user ID
            }
            throw std::runtime_error(\"Invalid credentials\");
        }
    ")
    list(APPEND BACKEND_SOURCES ${CMAKE_CURRENT_BINARY_DIR}/mock_auth_service.cpp)

    file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/mock_patient_service.cpp "
        #include \"../../src/backend/core/services/patient_service.h\"
        #include <iostream>
        PatientService::PatientService(std::shared_ptr<DBManager> db) : db_manager(db) {
            std::cout << \"Mock PatientService created\" << std::endl;
        }
        int PatientService::createPatient(const Patient& patient, int user_id, const std::string& ip, const std::string& session) {
            std::cout << \"Mock patient creation: \" << patient.first_name << \" \" << patient.last_name << std::endl;
            return 1; // Mock patient ID
        }
        Patient PatientService::getPatient(int patient_id, int user_id, const std::string& ip, const std::string& session) {
            std::cout << \"Mock patient retrieval for ID: \" << patient_id << std::endl;
            Patient mock_patient;
            mock_patient.id = patient_id;
            mock_patient.first_name = \"Mock\";
            mock_patient.last_name = \"Patient\";
            return mock_patient;
        }
    ")
    list(APPEND BACKEND_SOURCES ${CMAKE_CURRENT_BINARY_DIR}/mock_patient_service.cpp)
endif()

add_library(backend ${BACKEND_SOURCES})
set_property(TARGET backend PROPERTY POSITION_INDEPENDENT_CODE ON)

if(USE_POSTGRES)
    target_link_libraries(backend
        ${PostgreSQL_LIBRARIES}
        pybind11::module
        bcrypt
    )
else()
    target_link_libraries(backend
        pybind11::module
    )
endif()

# Pybind11 module
pybind11_add_module(medisys_bindings bindings/pybind_module.cpp)
target_link_libraries(medisys_bindings PRIVATE backend)

# Main executable
add_executable(medisys_main main.cpp)
target_link_libraries(medisys_main backend)

# Add compile definitions based on options
if(NOT USE_POSTGRES)
    target_compile_definitions(backend PRIVATE -DMOCK_DATABASE)
    target_compile_definitions(medisys_bindings PRIVATE -DMOCK_DATABASE)
    target_compile_definitions(medisys_main PRIVATE -DMOCK_DATABASE)
endif()