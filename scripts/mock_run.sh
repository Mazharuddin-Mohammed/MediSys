#!/bin/bash
set -e

echo "This is a mock run script that simulates running the MediSys application."
echo "In a real environment, you would have all dependencies installed and"
echo "would run ./scripts/run.sh to start the application."
echo ""

# Start mock backend
echo "Starting mock backend..."
echo "MediSys backend started" &

# Start mock frontend
echo "Starting mock frontend..."
python3 scripts/mock_frontend.py
