import sys
import uuid

from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QHBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import os
import sys

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
            user_id = auth_service.authenticate(username, password)
            ip_address = "192.168.1.1"  # TODO: Get from network context
            session_id = "session_" + str(uuid.uuid4())

            try:
                self.db.set_audit_context(user_id, ip_address, session_id)
            except Exception as audit_error:
                print(f"Warning: Could not set audit context: {audit_error}")

            self.error_label.setText("Login successful")
            self.password_input.clear()

            # Open appropriate window based on user role
            # For now, we'll just import and show the admin window as an example
            from gui.admin_window import AdminWindow
            self.admin_window = AdminWindow()
            self.admin_window.show()
            self.close()
        except Exception as e:
            print(f"Login error: {e}")
            self.error_label.setText(f"Login failed: {str(e)}")
            self.password_input.clear()