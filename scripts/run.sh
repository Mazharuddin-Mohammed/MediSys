#!/bin/bash
set -e

# Check if build directory exists
if [ ! -d "build" ]; then
    echo "Error: Build directory not found. Run ./scripts/build.sh first."
    exit 1
fi

# Check if backend executable exists
if [ ! -f "build/medisys_main" ]; then
    echo "Error: Backend executable not found. Run ./scripts/build.sh first."
    exit 1
fi

# Set database environment variables with defaults
export DB_NAME=${DB_NAME:-medisys}
export DB_USER=${DB_USER:-postgres}
export DB_PASS=${DB_PASS:-secret}
export DB_HOST=${DB_HOST:-localhost}

# Check if PostgreSQL is running
if command -v pg_isready >/dev/null 2>&1 && pg_isready -h $DB_HOST -U $DB_USER > /dev/null 2>&1; then
    echo "PostgreSQL is running. Starting MediSys with database: $DB_NAME on $DB_HOST"
else
    echo "PostgreSQL is not available. Starting MediSys with mock database."
fi

# Start backend
cd build
./medisys_main &
BACKEND_PID=$!

# Start frontend
echo "Starting frontend..."

# Check if PySide6 is available
if python3 -c "import PySide6" 2>/dev/null; then
    echo "PySide6 is available, starting full GUI frontend"
    python3 ../src/frontend/python/main.py
else
    echo "PySide6 is not available, starting simple frontend"
    python3 ../src/frontend/python/simple_main.py
fi

# Cleanup backend process when frontend exits
kill $BACKEND_PID 2>/dev/null || true