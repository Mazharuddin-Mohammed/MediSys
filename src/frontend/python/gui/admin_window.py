from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QTableView
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MediSys - Admin Dashboard")
        self.setMinimumSize(800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Banner
        banner_label = QLabel()
        banner_pixmap = QPixmap("resources/images/medisys_banner.png")
        banner_label.setPixmap(banner_pixmap.scaledToWidth(800, Qt.SmoothTransformation))
        banner_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(banner_label)

        # Placeholder for audit log view
        audit_label = QLabel("Audit Log")
        audit_table = QTableView()  # TODO: Populate with audit_summary view
        main_layout.addWidget(audit_label)
        main_layout.addWidget(audit_table)
        main_layout.addStretch()