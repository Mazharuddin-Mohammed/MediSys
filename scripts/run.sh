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

echo "Starting MediSys with database: $DB_NAME on $DB_HOST"

# Start backend
cd build
./medisys_main &
BACKEND_PID=$!

# Start frontend
echo "Starting frontend..."
python3 ../src/frontend/python/main.py

# Cleanup backend process when frontend exits
kill $BACKEND_PID 2>/dev/null || true