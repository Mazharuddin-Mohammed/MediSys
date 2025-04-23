"""
Admin Window Module for MediSys Hospital Management System

This module implements the main admin dashboard window with system overview,
audit log, and quick access to all other modules. It serves as the central
hub for system administration and monitoring.

Author: Mazharuddin Mohammed
"""

from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel,
                             QTableView, QPushButton, QTabWidget, QTreeView, QListWidget,
                             QGroupBox, QFormLayout, QLineEdit, QDateEdit, QComboBox,
                             QTextEdit, QMessageBox, QSplitter, QToolBar, QStatusBar)
from PySide6.QtGui import QPixmap, QIcon, QAction, QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt, QSize, QDate, Signal, Slot

class AdminWindow(QMainWindow):
    def __init__(self, db=None, user_id=None):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.setWindowTitle("MediSys - Admin Dashboard")
        self.setMinimumSize(1024, 768)

        # Create status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")

        # Create toolbar
        self.toolbar = QToolBar("Main Toolbar")
        self.toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(self.toolbar)

        # Add toolbar actions
        self.action_patients = QAction("Patients")
        self.action_patients.triggered.connect(self.show_patients)
        self.toolbar.addAction(self.action_patients)

        self.action_departments = QAction("Departments")
        self.action_departments.triggered.connect(self.show_departments)
        self.toolbar.addAction(self.action_departments)

        self.action_doctors = QAction("Doctors")
        self.action_doctors.triggered.connect(self.show_doctors)
        self.toolbar.addAction(self.action_doctors)

        self.action_appointments = QAction("Appointments")
        self.action_appointments.triggered.connect(self.show_appointments)
        self.toolbar.addAction(self.action_appointments)

        self.action_reports = QAction("Reports")
        self.action_reports.triggered.connect(self.show_reports)
        self.toolbar.addAction(self.action_reports)

        self.action_audit = QAction("Audit Log")
        self.action_audit.triggered.connect(self.show_audit)
        self.toolbar.addAction(self.action_audit)

        # Create central widget with tab interface
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Banner
        banner_label = QLabel()
        banner_pixmap = QPixmap("src/frontend/python/resources/images/banner.jpg")
        banner_label.setPixmap(banner_pixmap.scaledToWidth(800, Qt.SmoothTransformation))
        banner_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(banner_label)

        # Tab widget
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # Dashboard tab
        dashboard_widget = QWidget()
        dashboard_layout = QVBoxLayout(dashboard_widget)
        dashboard_label = QLabel("Welcome to MediSys Admin Dashboard")
        dashboard_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        dashboard_layout.addWidget(dashboard_label)

        # Dashboard stats
        stats_layout = QHBoxLayout()

        # Patients stats
        patients_box = QGroupBox("Patients")
        patients_layout = QVBoxLayout(patients_box)
        patients_count = QLabel("Total: 0")
        patients_today = QLabel("Today: 0")
        patients_layout.addWidget(patients_count)
        patients_layout.addWidget(patients_today)
        stats_layout.addWidget(patients_box)

        # Appointments stats
        appointments_box = QGroupBox("Appointments")
        appointments_layout = QVBoxLayout(appointments_box)
        appointments_count = QLabel("Total: 0")
        appointments_today = QLabel("Today: 0")
        appointments_layout.addWidget(appointments_count)
        appointments_layout.addWidget(appointments_today)
        stats_layout.addWidget(appointments_box)

        # Doctors stats
        doctors_box = QGroupBox("Doctors")
        doctors_layout = QVBoxLayout(doctors_box)
        doctors_count = QLabel("Total: 0")
        doctors_active = QLabel("Active: 0")
        doctors_layout.addWidget(doctors_count)
        doctors_layout.addWidget(doctors_active)
        stats_layout.addWidget(doctors_box)

        dashboard_layout.addLayout(stats_layout)
        dashboard_layout.addStretch()

        # System Overview tab
        overview_widget = QWidget()
        overview_layout = QVBoxLayout(overview_widget)

        # Welcome message
        welcome_label = QLabel("Welcome to MediSys Admin Dashboard")
        welcome_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        welcome_label.setAlignment(Qt.AlignCenter)
        overview_layout.addWidget(welcome_label)

        # System stats
        stats_layout = QHBoxLayout()

        # Users stats
        users_box = QGroupBox("System Users")
        users_layout = QVBoxLayout(users_box)
        users_count = QLabel("Total Users: 15")
        users_active = QLabel("Active Now: 3")
        users_layout.addWidget(users_count)
        users_layout.addWidget(users_active)
        stats_layout.addWidget(users_box)

        # Database stats
        db_box = QGroupBox("Database")
        db_layout = QVBoxLayout(db_box)
        db_status = QLabel("Status: Connected")
        db_size = QLabel("Size: 256 MB")
        db_layout.addWidget(db_status)
        db_layout.addWidget(db_size)
        stats_layout.addWidget(db_box)

        # System stats
        system_box = QGroupBox("System")
        system_layout = QVBoxLayout(system_box)
        system_uptime = QLabel("Uptime: 15 days")
        system_version = QLabel("Version: 1.0.0")
        system_layout.addWidget(system_uptime)
        system_layout.addWidget(system_version)
        stats_layout.addWidget(system_box)

        overview_layout.addLayout(stats_layout)

        # Quick access buttons
        quick_access_label = QLabel("Quick Access")
        quick_access_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        overview_layout.addWidget(quick_access_label)

        quick_buttons_layout = QHBoxLayout()

        patients_button = QPushButton("Patients")
        patients_button.clicked.connect(self.show_patients)
        quick_buttons_layout.addWidget(patients_button)

        departments_button = QPushButton("Departments")
        departments_button.clicked.connect(self.show_departments)
        quick_buttons_layout.addWidget(departments_button)

        doctors_button = QPushButton("Doctors")
        doctors_button.clicked.connect(self.show_doctors)
        quick_buttons_layout.addWidget(doctors_button)

        appointments_button = QPushButton("Appointments")
        appointments_button.clicked.connect(self.show_appointments)
        quick_buttons_layout.addWidget(appointments_button)

        reports_button = QPushButton("Reports")
        reports_button.clicked.connect(self.show_reports)
        quick_buttons_layout.addWidget(reports_button)

        overview_layout.addLayout(quick_buttons_layout)
        overview_layout.addStretch()

        # Audit log tab
        audit_widget = QWidget()
        audit_layout = QVBoxLayout(audit_widget)
        audit_label = QLabel("Audit Log")
        audit_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        audit_layout.addWidget(audit_label)

        # Audit table
        audit_table = QTableView()
        audit_model = QStandardItemModel(0, 6)
        audit_model.setHorizontalHeaderLabels(["Timestamp", "User", "Action", "Entity", "Entity ID", "Details"])
        audit_table.setModel(audit_model)
        audit_layout.addWidget(audit_table)

        # Add tabs
        self.tabs.addTab(dashboard_widget, "Dashboard")
        self.tabs.addTab(overview_widget, "System Overview")
        self.tabs.addTab(audit_widget, "Audit Log")

        # Add some sample data
        self.add_sample_data()

    def add_sample_data(self):
        """Add sample data to the tables for demonstration purposes"""
        # Add sample audit entries
        audit_table = None
        for table in self.findChildren(QTableView):
            if table.parent() and isinstance(table.parent(), QWidget) and table.parent().layout() and isinstance(table.parent().layout(), QVBoxLayout):
                # Check if this table is in the audit tab
                if self.tabs.indexOf(table.parent()) == 2:  # Audit tab index
                    audit_table = table
                    break

        if audit_table and audit_table.model():
            audit_model = audit_table.model()
            for i in range(5):
                row_items = [
                    QStandardItem(f"2023-06-{i+1} 10:0{i}:00"),
                    QStandardItem("admin"),
                    QStandardItem("login" if i == 0 else "view" if i % 2 == 0 else "edit"),
                    QStandardItem("user" if i == 0 else "patient"),
                    QStandardItem(str(i)),
                    QStandardItem(f"Sample audit entry {i+1}")
                ]
                audit_model.appendRow(row_items)

    def show_patients(self):
        from gui.patients_window import PatientsWindow
        self.patients_window = PatientsWindow(db=self.db, user_id=self.user_id)
        self.patients_window.show()
        self.statusBar.showMessage("Opened Patients module")

    def show_departments(self):
        from gui.departments_window import DepartmentsWindow
        self.departments_window = DepartmentsWindow(db=self.db, user_id=self.user_id)
        self.departments_window.show()
        self.statusBar.showMessage("Opened Departments module")

    def show_doctors(self):
        from gui.doctors_window import DoctorsWindow
        self.doctors_window = DoctorsWindow(db=self.db, user_id=self.user_id)
        self.doctors_window.show()
        self.statusBar.showMessage("Opened Doctors module")

    def show_appointments(self):
        from gui.appointments_window import AppointmentsWindow
        self.appointments_window = AppointmentsWindow(db=self.db, user_id=self.user_id)
        self.appointments_window.show()
        self.statusBar.showMessage("Opened Appointments module")

    def show_reports(self):
        from gui.reports_window import ReportsWindow
        self.reports_window = ReportsWindow(db=self.db, user_id=self.user_id)
        self.reports_window.show()
        self.statusBar.showMessage("Opened Reports module")

    def show_audit(self):
        self.tabs.setCurrentIndex(2)  # Switch to Audit tab
        self.statusBar.showMessage("Viewing audit log")

