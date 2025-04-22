cmake_minimum_required(VERSION 3.20)
project(MediSys)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find dependencies
find_package(PostgreSQL REQUIRED)
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 REQUIRED)

# Find Catch2 for testing
find_package(Catch2 QUIET)
if(NOT Catch2_FOUND)
    include(FetchContent)
    FetchContent_Declare(
        Catch2
        GIT_REPOSITORY https://github.com/catchorg/Catch2.git
        GIT_TAG v2.13.7
    )
    FetchContent_MakeAvailable(Catch2)
endif()

# Include directories
include_directories(${PostgreSQL_INCLUDE_DIRS})
include_directories(${Python3_INCLUDE_DIRS})
include_directories(src/backend)

# Add subdirectories
add_subdirectory(src/backend)
add_subdirectory(src/frontend)

# Enable testing
enable_testing()
add_subdirectory(src/tests)