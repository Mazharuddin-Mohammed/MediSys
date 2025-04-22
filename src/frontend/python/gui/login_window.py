from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QHBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import uuid
import medisys_bindings

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
        banner_pixmap = QPixmap("resources/images/medisys_banner.png")
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
            self.db.set_audit_context(user_id, ip_address, session_id)
            self.error_label.setText("Login successful")  # TODO: Open main window
            self.password_input.clear()
        except Exception as e:
            self.error_label.setText("Login failed")
            self.password_input.clear()