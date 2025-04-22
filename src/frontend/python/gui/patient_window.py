from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class PatientWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MediSys - Patient Portal")
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

        # Placeholder
        main_layout.addWidget(QLabel("Patient Portal Placeholder"))
        main_layout.addStretch()