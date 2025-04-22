#!/usr/bin/env python3

print("MediSys Frontend Simulation")
print("===========================")
print("1. Loading configuration...")
print("2. Connecting to database...")
print("3. Initializing UI components...")
print("4. Starting application...")
print("\nMediSys Login Window")
print("-------------------")
print("Username: [admin]")
print("Password: [********]")
print("\n[Login button clicked]")
print("Authentication successful!")
print("\nMediSys Admin Dashboard")
print("----------------------")
print("- Users: 5")
print("- Departments: 3")
print("- Doctors: 10")
print("- Patients: 25")
print("- Recent Activity:")
print("  * User 'admin' logged in at 2023-04-22 15:30:45")
print("  * Patient 'John Doe' registered at 2023-04-22 14:25:10")
print("  * Doctor 'Jane Smith' added to Cardiology department at 2023-04-22 13:15:22")
print("\nApplication running successfully!")
print("Press Ctrl+C to exit...")

# Simulate running application
import time
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nApplication shutting down...")
    print("Goodbye!")
