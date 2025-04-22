cmake_minimum_required(VERSION 3.10)

# Backend tests
if(USE_POSTGRES)
    add_executable(test_db_manager backend_tests/test_db_manager.cpp)
    target_link_libraries(test_db_manager backend Catch2::Catch2)
    add_test(NAME test_db_manager COMMAND test_db_manager)

    add_executable(test_auth_service backend_tests/test_auth_service.cpp)
    target_link_libraries(test_auth_service backend Catch2::Catch2)
    add_test(NAME test_auth_service COMMAND test_auth_service)
endif()

# Frontend tests
# Python tests are run separately using unittest
