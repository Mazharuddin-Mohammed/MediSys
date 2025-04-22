#!/bin/bash
set -e

# Set database environment variables with defaults
DB_NAME=${DB_NAME:-medisys}
DB_USER=${DB_USER:-postgres}
DB_PASS=${DB_PASS:-secret}

# Check if psql is available
command -v psql >/dev/null 2>&1 || { echo "Error: PostgreSQL client (psql) is required but not installed."; exit 1; }

# Set PGPASSWORD environment variable if DB_PASS is provided
if [ -n "$DB_PASS" ]; then
    export PGPASSWORD="$DB_PASS"
fi

echo "Setting up database: $DB_NAME"

# Check if database already exists
if psql -U "$DB_USER" -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    echo "Database $DB_NAME already exists. Do you want to drop and recreate it? (y/N)"
    read -r answer
    if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
        echo "Dropping database $DB_NAME..."
        psql -U "$DB_USER" -c "DROP DATABASE $DB_NAME;"
    else
        echo "Keeping existing database. Schema will be reapplied."
    fi
fi

# Create database if it doesn't exist
if ! psql -U "$DB_USER" -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    echo "Creating database $DB_NAME..."
    psql -U "$DB_USER" -c "CREATE DATABASE $DB_NAME;"
fi

# Apply schema
echo "Applying schema to $DB_NAME..."
psql -U "$DB_USER" -d "$DB_NAME" -f src/backend/core/database/schema.sql

echo "Database setup completed successfully!"