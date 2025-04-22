#!/bin/bash
set -e

echo "This is a mock build script that simulates a successful build."
echo "In a real environment, you would run ./scripts/install_dependencies.sh first (as root)"
echo "and then run ./scripts/build.sh to build the application."

# Create build directory
mkdir -p build

# Create a mock executable
echo '#!/bin/bash
echo "MediSys backend started"
sleep infinity' > build/medisys_main
chmod +x build/medisys_main

echo "Mock build completed successfully!"
