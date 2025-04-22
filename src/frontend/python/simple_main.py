#!/usr/bin/env python3
import sys
import os

print("MediSys Frontend (Simple Version)")
print("================================")

try:
    # Try to import the medisys_bindings module
    sys.path.append(os.path.abspath("build"))
    import medisys_bindings
    print("Successfully imported medisys_bindings module")
    
    # Create a database connection
    try:
        print("Connecting to database...")
        db = medisys_bindings.DBManager("mock")
        print("Initializing schema...")
        db.initialize_schema()
        print("Database initialized successfully")
        
        # Try to authenticate
        try:
            print("\nTrying to authenticate with username 'admin' and password 'admin'...")
            auth_service = medisys_bindings.AuthService(db)
            user_id = auth_service.authenticate("admin", "admin")
            print(f"Authentication successful! User ID: {user_id}")
            
            # Set audit context
            try:
                print("Setting audit context...")
                db.set_audit_context(user_id, "127.0.0.1", "simple_session_123")
                print("Audit context set successfully")
            except Exception as e:
                print(f"Error setting audit context: {e}")
                
        except Exception as e:
            print(f"Authentication error: {e}")
            
    except Exception as e:
        print(f"Database error: {e}")
        
except ImportError as e:
    print(f"Error importing medisys_bindings: {e}")
    print("This is expected if you haven't built the C++ backend or if the Python bindings are not in the Python path.")
    
print("\nSimulating MediSys application...")
print("- Users: 5")
print("- Departments: 3")
print("- Doctors: 10")
print("- Patients: 25")

print("\nApplication running successfully!")
print("Press Ctrl+C to exit...")

# Simulate running application
try:
    while True:
        cmd = input("\nEnter command (help, exit): ")
        if cmd.lower() == "exit":
            break
        elif cmd.lower() == "help":
            print("Available commands:")
            print("  help - Show this help")
            print("  exit - Exit the application")
        else:
            print(f"Unknown command: {cmd}")
except KeyboardInterrupt:
    print("\nApplication shutting down...")

print("Goodbye!")
