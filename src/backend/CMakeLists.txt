set(BACKEND_SOURCES
    core/models/user.cpp
    core/models/patient.cpp
    core/models/doctor.cpp
    core/models/department.cpp
    core/database/db_manager.cpp
    core/services/auth_service.cpp
    core/services/patient_service.cpp
)

add_library(backend ${BACKEND_SOURCES})
set_property(TARGET backend PROPERTY POSITION_INDEPENDENT_CODE ON)

# Find OpenSSL
find_package(OpenSSL REQUIRED)

target_link_libraries(backend
    ${PostgreSQL_LIBRARIES}
    pybind11::module
    OpenSSL::SSL
    OpenSSL::Crypto
    pqxx
)

# Pybind11 module
pybind11_add_module(medisys_bindings bindings/pybind_module.cpp)
target_link_libraries(medisys_bindings PRIVATE backend)

# Main executable
add_executable(medisys_main main.cpp)
target_link_libraries(medisys_main backend)

