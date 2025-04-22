import sys
import uuid
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QVulkanInstance, QIcon
from gui.login_window import LoginWindow
import medisys_bindings

def main():
    app = QApplication(sys.argv)
    
    # Set application icon
    app.setWindowIcon(QIcon("resources/images/medisys_logo.png"))

    # Initialize Vulkan
    vulkan_instance = QVulkanInstance()
    if not vulkan_instance.create():
        print("Failed to initialize Vulkan")
        sys.exit(1)
    app.setVulkanInstance(vulkan_instance)

    # Load stylesheet
    with open("resources/styles/theme.qss", "r") as f:
        app.setStyleSheet(f.read())

    # Initialize database
    db = medisys_bindings.DBManager("dbname=medisys user=postgres password=secret host=localhost")
    db.initialize_schema()

    # Show login window
    login_window = LoginWindow(db)
    login_window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()