"""
Login Window Module for MediSys Hospital Management System

This module implements the login window that authenticates users and provides
access to the appropriate modules based on user role. It handles authentication
through the C++ backend and sets up the audit context for tracking user actions.

Author: Mazharuddin Mohammed
"""

import sys
import uuid
import os

from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QHBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

# Try to import medisys_bindings from different locations
try:
    import medisys_bindings
except ImportError:
    # Try to import from the parent directory
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    try:
        import medisys_bindings
    except ImportError:
        # Try to import from the build directory
        build_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "build"))
        sys.path.insert(0, build_dir)
        try:
            import medisys_bindings
        except ImportError:
            print("Error: Could not import medisys_bindings module.")
            print("Python path:", sys.path)
            sys.exit(1)

class LoginWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("MediSys - Login")
        self.setMinimumSize(400, 300)

        # Setup UI
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Banner
        banner_label = QLabel()
        banner_pixmap = QPixmap("src/frontend/python/resources/images/banner.jpg")
        banner_label.setPixmap(banner_pixmap.scaledToWidth(400, Qt.SmoothTransformation))
        banner_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(banner_label)

        # Form
        form_layout = QVBoxLayout()
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Login")
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red")

        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.login_button)
        form_layout.addWidget(self.error_label)
        main_layout.addLayout(form_layout)
        main_layout.addStretch()

        # Connect signals
        self.login_button.clicked.connect(self.handle_login)

        # Enable Enter key for login
        self.password_input.returnPressed.connect(self.handle_login)

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        if not (username and password):
            self.error_label.setText("Username and password are required")
            return
        if len(username) > 50 or len(password) > 255:
            self.error_label.setText("Input too long")
            return
        try:
            auth_service = medisys_bindings.AuthService(self.db)
            auth_result = auth_service.authenticate(username, password)

            # In a real implementation, auth_result would be a dictionary with user info
            # For now, we'll just get the user_id and assume a role based on the username
            if isinstance(auth_result, dict):
                user_id = auth_result.get("user_id")
                # Role should come from the auth_result, but for now we'll determine it from the username
            else:
                # If auth_result is just the user_id (current implementation)
                user_id = auth_result
                # For testing, we'll determine role based on username
                if username.lower() == "admin":
                    auth_result = {"role": "admin", "user_id": user_id}
                elif username.lower().startswith("doc"):
                    auth_result = {"role": "doctor", "user_id": user_id}
                elif username.lower().startswith("pat"):
                    auth_result = {"role": "patient", "user_id": user_id}
                else:
                    auth_result = {"role": "admin", "user_id": user_id}  # Default to admin

            ip_address = "192.168.1.1"  # TODO: Get from network context
            session_id = "session_" + str(uuid.uuid4())

            try:
                # Make sure user_id is valid before setting audit context
                if user_id and user_id > 0:
                    self.db.set_audit_context(user_id, ip_address, session_id)
                else:
                    print("Warning: Invalid user_id for audit context")
            except Exception as audit_error:
                print(f"Warning: Could not set audit context: {audit_error}")

            self.error_label.setText("Login successful")
            self.password_input.clear()

            # Open appropriate window based on user role
            user_role = auth_result.get("role", "").lower()

            if user_role == "admin":
                from gui.admin_window import AdminWindow
                self.next_window = AdminWindow(db=self.db, user_id=user_id)
            elif user_role == "doctor":
                from gui.doctor_window import DoctorWindow
                self.next_window = DoctorWindow(db=self.db, user_id=user_id)
            elif user_role == "patient":
                from gui.patient_window import PatientWindow
                self.next_window = PatientWindow()
            else:
                # Default to admin window if role is unknown
                from gui.admin_window import AdminWindow
                self.next_window = AdminWindow(db=self.db, user_id=user_id)

            self.next_window.show()
            self.close()
        except Exception as e:
            print(f"Login error: {e}")
            self.error_label.setText(f"Login failed: {str(e)}")
            self.password_input.clear()