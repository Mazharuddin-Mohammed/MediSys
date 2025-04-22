import sys
import os
import uuid

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Now we can import our modules
from gui.login_window import LoginWindow

# Try to import medisys_bindings from different locations
try:
    import medisys_bindings
except ImportError:
    # Try to import from the build directory
    build_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "build"))
    sys.path.insert(0, build_dir)
    try:
        import medisys_bindings
    except ImportError:
        print("Error: Could not import medisys_bindings module.")
        print("Python path:", sys.path)
        sys.exit(1)

def main():
    app = QApplication(sys.argv)

    # Set application icon
    app.setWindowIcon(QIcon("src/frontend/python/resources/images/logo.jpg"))

    # Vulkan initialization removed - using default rendering

    # Load stylesheet
    with open("src/frontend/python/resources/styles/theme.qss", "r") as f:
        app.setStyleSheet(f.read())

    # Initialize database using environment variables or defaults
    import os

    # Connect to the database
    db_name = os.environ.get('DB_NAME', 'medisys')
    db_user = os.environ.get('DB_USER', 'postgres')
    db_pass = os.environ.get('DB_PASS', 'secret')
    db_host = os.environ.get('DB_HOST', 'localhost')

    conn_str = f"dbname={db_name} user={db_user} password={db_pass} host={db_host}"
    print(f"Connecting to database: {conn_str}")
    db = medisys_bindings.DBManager(conn_str)
    db.initialize_schema()
    print("Database initialized successfully")

    # Show login window
    login_window = LoginWindow(db)
    login_window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()