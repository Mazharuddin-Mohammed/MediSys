#!/bin/bash
set -e

echo "Installing MediSys dependencies..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root or with sudo"
  exit 1
fi

# Update package lists
apt-get update

# Install PostgreSQL and development libraries
apt-get install -y postgresql postgresql-contrib libpq-dev

# Install Python and development libraries
apt-get install -y python3 python3-dev python3-pip

# Install C++ development tools
apt-get install -y build-essential cmake cppcheck

# Install bcrypt library
apt-get install -y libbcrypt-dev

# Install Python dependencies
pip3 install -r requirements.txt

echo "All dependencies installed successfully!"
