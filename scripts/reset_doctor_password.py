#!/usr/bin/env python3
"""
Reset Doctor Password Utility

This script resets the password for the doctor user in the MediSys database.
It calculates the SHA-256 hash of 'doctor123' and updates the database directly.

Usage:
    python3 reset_doctor_password.py

Author: Mazharuddin Mohammed
"""

import sys
import os
import hashlib
import psycopg2
from psycopg2 import sql

def main():
    # Calculate the SHA-256 hash of 'doctor123'
    password = 'doctor123'
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    print(f"Calculated hash for 'doctor123': {password_hash}")
    
    # Connect to the database
    try:
        conn = psycopg2.connect(
            dbname="medisys",
            user="postgres",
            password="secret",
            host="localhost"
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Update the doctor user's password hash
        cursor.execute(
            "UPDATE users SET password_hash = %s WHERE username = 'doctor'",
            (password_hash,)
        )
        
        # Check if the update was successful
        if cursor.rowcount > 0:
            print("Doctor password reset successfully!")
        else:
            print("Doctor user not found. Creating new doctor user...")
            
            # Create the doctor user if it doesn't exist
            cursor.execute(
                """
                INSERT INTO users (username, password_hash, email, role, first_name, last_name)
                VALUES ('doctor', %s, 'doctor@medisys.com', 'doctor', 'John', 'Smith')
                ON CONFLICT (username) DO NOTHING
                """,
                (password_hash,)
            )
            
            if cursor.rowcount > 0:
                print("Doctor user created successfully!")
            else:
                print("Failed to create doctor user.")
        
        # Verify the password hash in the database
        cursor.execute("SELECT password_hash FROM users WHERE username = 'doctor'")
        result = cursor.fetchone()
        
        if result:
            db_hash = result[0]
            print(f"Current hash in database: {db_hash}")
            if db_hash == password_hash:
                print("Password hash verification successful!")
            else:
                print("Warning: Database hash does not match calculated hash!")
        else:
            print("Error: Could not retrieve doctor user from database.")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
