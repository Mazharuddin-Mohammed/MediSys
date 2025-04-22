cmake_minimum_required(VERSION 3.20)
project(MediSys)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find dependencies
find_package(PostgreSQL REQUIRED)
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 REQUIRED)

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