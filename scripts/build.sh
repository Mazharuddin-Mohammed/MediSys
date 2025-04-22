#!/bin/bash
set -e

# Check for required tools
command -v cmake >/dev/null 2>&1 || { echo "Error: cmake is required but not installed."; exit 1; }
command -v make >/dev/null 2>&1 || { echo "Error: make is required but not installed."; exit 1; }

# Create build directory
mkdir -p build
cd build

# Configure and build
echo "Configuring with CMake..."

# Check if PostgreSQL is available
if command -v pg_config >/dev/null 2>&1; then
    echo "PostgreSQL development files found, building with database support"
    cmake ..
else
    echo "PostgreSQL development files not found. Please install PostgreSQL development files."
    echo "On Ubuntu/Debian: sudo apt-get install libpq-dev"
    echo "On Fedora/RHEL: sudo dnf install postgresql-devel"
    echo "On macOS: brew install postgresql"
    exit 1
fi

echo "Building..."
make -j$(nproc)
cd ..

# Run static analysis if tools are available
if command -v cppcheck >/dev/null 2>&1; then
    echo "Running cppcheck..."
    cppcheck --enable=all src/backend
else
    echo "Warning: cppcheck not found, skipping C++ static analysis."
fi

if command -v pylint >/dev/null 2>&1; then
    echo "Running pylint..."
    pylint src/frontend/python || echo "Pylint found issues, but continuing build."
else
    echo "Warning: pylint not found, skipping Python static analysis."
fi

echo "Build completed successfully!"