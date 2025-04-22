cmake_minimum_required(VERSION 3.20)
project(MediSys)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find dependencies
option(USE_POSTGRES "Use PostgreSQL database" ON)
option(BUILD_TESTS "Build tests" ON)

# Find Python
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)

# Find pybind11
find_package(pybind11 QUIET)
if(NOT pybind11_FOUND)
    include(FetchContent)
    FetchContent_Declare(
        pybind11
        GIT_REPOSITORY https://github.com/pybind/pybind11.git
        GIT_TAG v2.10.0
    )
    FetchContent_MakeAvailable(pybind11)
endif()

# Find PostgreSQL if enabled
if(USE_POSTGRES)
    find_package(PostgreSQL QUIET)
    if(PostgreSQL_FOUND)
        add_definitions(-DUSE_POSTGRES)
        message(STATUS "PostgreSQL found, building with database support")
    else()
        message(WARNING "PostgreSQL not found, building without database support")
        set(USE_POSTGRES OFF)
    endif()
endif()

# Find Catch2 for testing if tests are enabled
if(BUILD_TESTS)
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
endif()

# Include directories
if(PostgreSQL_FOUND)
    include_directories(${PostgreSQL_INCLUDE_DIRS})
endif()
include_directories(${Python3_INCLUDE_DIRS})
include_directories(src/backend)

# Add subdirectories
add_subdirectory(src/backend)
add_subdirectory(src/frontend)

# Enable testing if requested
if(BUILD_TESTS)
    enable_testing()
    add_subdirectory(src/tests)
endif()