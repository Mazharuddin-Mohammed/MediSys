import sys
import uuid
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QVulkanInstance, QIcon
from gui.login_window import LoginWindow
import medisys_bindings

def main():
    app = QApplication(sys.argv)

    # Set application icon
    app.setWindowIcon(QIcon("src/frontend/python/resources/images/logo.jpg"))

    # Initialize Vulkan
    vulkan_instance = QVulkanInstance()
    if not vulkan_instance.create():
        print("Failed to initialize Vulkan")
        sys.exit(1)
    app.setVulkanInstance(vulkan_instance)

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