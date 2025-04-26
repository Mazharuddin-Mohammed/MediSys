"""
Doctor Window Module for MediSys Hospital Management System

This module implements the doctor dashboard window that provides doctors with
access to their patient lists, appointments, and medical record management.
Currently a placeholder for future implementation.

Author: Mazharuddin Mohammed
"""

from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel,
                             QTableView, QPushButton, QTabWidget, QCalendarWidget, QSplitter,
                             QToolBar, QStatusBar, QComboBox, QLineEdit, QFormLayout, QTextEdit)
from PySide6.QtGui import QPixmap, QIcon, QAction, QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt, QSize, QDate, Signal, Slot
import os
import base64

class DoctorWindow(QMainWindow):
    def __init__(self, db=None, user_id=None):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.setWindowTitle("MediSys - Doctor Dashboard")
        self.setMinimumSize(1024, 768)

        # Create status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Welcome, Doctor")

        # Create toolbar
        self.toolbar = QToolBar("Main Toolbar")
        self.toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(self.toolbar)

        # Add toolbar actions
        self.action_patients = QAction("My Patients")
        self.action_patients.triggered.connect(self.show_patients)
        self.toolbar.addAction(self.action_patients)

        self.action_appointments = QAction("Appointments")
        self.action_appointments.triggered.connect(self.show_appointments)
        self.toolbar.addAction(self.action_appointments)

        self.action_prescriptions = QAction("Prescriptions")
        self.action_prescriptions.triggered.connect(self.show_prescriptions)
        self.toolbar.addAction(self.action_prescriptions)

        self.action_profile = QAction("My Profile")
        self.action_profile.triggered.connect(self.show_profile)
        self.toolbar.addAction(self.action_profile)

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

        welcome_label = QLabel("Welcome to your Doctor Dashboard")
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        welcome_label.setAlignment(Qt.AlignCenter)
        dashboard_layout.addWidget(welcome_label)

        # Today's appointments section
        appointments_label = QLabel("Today's Appointments")
        appointments_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        dashboard_layout.addWidget(appointments_label)

        # Appointments table
        self.today_appointments_table = QTableView()
        self.today_appointments_model = QStandardItemModel(0, 5)
        self.today_appointments_model.setHorizontalHeaderLabels([
            "Time", "Patient Name", "Reason", "Status", "Room"
        ])
        self.today_appointments_table.setModel(self.today_appointments_model)
        dashboard_layout.addWidget(self.today_appointments_table)

        # Add sample appointments
        self.add_sample_appointments()

        # Add dashboard tab
        self.tabs.addTab(dashboard_widget, "Dashboard")

        # Add other tabs
        self.setup_patients_tab()
        self.setup_appointments_tab()
        self.setup_prescriptions_tab()

    def add_sample_appointments(self):
        """Add sample appointments to the dashboard"""
        appointments = [
            ["09:00 AM", "John Smith", "Follow-up", "Scheduled", "Room 101"],
            ["10:30 AM", "Jane Doe", "Consultation", "Checked In", "Room 102"],
            ["01:15 PM", "Robert Johnson", "Annual Physical", "Scheduled", "Room 103"],
            ["03:00 PM", "Emily Davis", "Lab Results", "Scheduled", "Room 101"],
            ["04:30 PM", "Michael Brown", "Follow-up", "Scheduled", "Room 102"]
        ]

        for appointment in appointments:
            row_items = [QStandardItem(item) for item in appointment]
            self.today_appointments_model.appendRow(row_items)

        self.today_appointments_table.resizeColumnsToContents()

    def setup_patients_tab(self):
        """Set up the patients tab"""
        patients_widget = QWidget()
        patients_layout = QVBoxLayout(patients_widget)

        # Search bar
        search_layout = QHBoxLayout()
        search_label = QLabel("Search Patients:")
        search_input = QLineEdit()
        search_button = QPushButton("Search")

        search_layout.addWidget(search_label)
        search_layout.addWidget(search_input)
        search_layout.addWidget(search_button)

        patients_layout.addLayout(search_layout)

        # Patients table
        self.patients_table = QTableView()
        self.patients_model = QStandardItemModel(0, 5)
        self.patients_model.setHorizontalHeaderLabels([
            "ID", "Name", "Age", "Last Visit", "Condition"
        ])
        self.patients_table.setModel(self.patients_model)

        patients_layout.addWidget(self.patients_table)

        # Add sample patients
        self.add_sample_patients()

        # Patient details button
        view_details_button = QPushButton("View Patient Details")
        view_details_button.clicked.connect(self.view_patient_details)
        patients_layout.addWidget(view_details_button)

        self.tabs.addTab(patients_widget, "My Patients")

    def add_sample_patients(self):
        """Add sample patients to the table"""
        patients = [
            ["P001", "John Smith", "45", "2023-05-15", "Hypertension"],
            ["P002", "Jane Doe", "32", "2023-05-20", "Diabetes Type 2"],
            ["P003", "Robert Johnson", "58", "2023-05-25", "Arthritis"],
            ["P004", "Emily Davis", "27", "2023-06-02", "Asthma"],
            ["P005", "Michael Brown", "41", "2023-06-10", "Anxiety"]
        ]

        for patient in patients:
            row_items = [QStandardItem(item) for item in patient]
            self.patients_model.appendRow(row_items)

        self.patients_table.resizeColumnsToContents()

    def setup_appointments_tab(self):
        """Set up the appointments tab"""
        appointments_widget = QWidget()
        appointments_layout = QVBoxLayout(appointments_widget)

        # Calendar and appointments split view
        splitter = QSplitter(Qt.Horizontal)

        # Calendar widget
        calendar_widget = QCalendarWidget()
        calendar_widget.setGridVisible(True)
        calendar_widget.setMinimumWidth(400)
        splitter.addWidget(calendar_widget)

        # Appointments for selected date
        appointments_for_date_widget = QWidget()
        appointments_for_date_layout = QVBoxLayout(appointments_for_date_widget)

        date_label = QLabel("Appointments for Selected Date")
        date_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        appointments_for_date_layout.addWidget(date_label)

        self.date_appointments_table = QTableView()
        self.date_appointments_model = QStandardItemModel(0, 5)
        self.date_appointments_model.setHorizontalHeaderLabels([
            "Time", "Patient Name", "Reason", "Status", "Room"
        ])
        self.date_appointments_table.setModel(self.date_appointments_model)
        appointments_for_date_layout.addWidget(self.date_appointments_table)

        splitter.addWidget(appointments_for_date_widget)

        appointments_layout.addWidget(splitter)

        self.tabs.addTab(appointments_widget, "Appointments")

    def setup_prescriptions_tab(self):
        """Set up the prescriptions tab"""
        prescriptions_widget = QWidget()
        prescriptions_layout = QVBoxLayout(prescriptions_widget)

        # Search bar
        search_layout = QHBoxLayout()
        search_label = QLabel("Search Prescriptions:")
        search_input = QLineEdit()
        search_button = QPushButton("Search")

        search_layout.addWidget(search_label)
        search_layout.addWidget(search_input)
        search_layout.addWidget(search_button)

        prescriptions_layout.addLayout(search_layout)

        # Prescriptions table
        self.prescriptions_table = QTableView()
        self.prescriptions_model = QStandardItemModel(0, 5)
        self.prescriptions_model.setHorizontalHeaderLabels([
            "ID", "Patient", "Medication", "Dosage", "Date Prescribed"
        ])
        self.prescriptions_table.setModel(self.prescriptions_model)

        prescriptions_layout.addWidget(self.prescriptions_table)

        # Add sample prescriptions
        self.add_sample_prescriptions()

        # New prescription button
        new_prescription_button = QPushButton("New Prescription")
        new_prescription_button.clicked.connect(self.new_prescription)
        prescriptions_layout.addWidget(new_prescription_button)

        self.tabs.addTab(prescriptions_widget, "Prescriptions")

    def add_sample_prescriptions(self):
        """Add sample prescriptions to the table"""
        prescriptions = [
            ["RX001", "John Smith", "Lisinopril", "10mg daily", "2023-05-15"],
            ["RX002", "Jane Doe", "Metformin", "500mg twice daily", "2023-05-20"],
            ["RX003", "Robert Johnson", "Ibuprofen", "400mg as needed", "2023-05-25"],
            ["RX004", "Emily Davis", "Albuterol", "2 puffs as needed", "2023-06-02"],
            ["RX005", "Michael Brown", "Sertraline", "50mg daily", "2023-06-10"]
        ]

        for prescription in prescriptions:
            row_items = [QStandardItem(item) for item in prescription]
            self.prescriptions_model.appendRow(row_items)

        self.prescriptions_table.resizeColumnsToContents()

    def show_patients(self):
        """Switch to patients tab"""
        self.tabs.setCurrentIndex(1)  # Patients tab
        self.statusBar.showMessage("Viewing patients")

    def show_appointments(self):
        """Switch to appointments tab"""
        self.tabs.setCurrentIndex(2)  # Appointments tab
        self.statusBar.showMessage("Viewing appointments")

    def show_prescriptions(self):
        """Switch to prescriptions tab"""
        self.tabs.setCurrentIndex(3)  # Prescriptions tab
        self.statusBar.showMessage("Viewing prescriptions")

    def show_profile(self):
        """Show doctor profile dialog"""
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel

        profile_dialog = QDialog(self)
        profile_dialog.setWindowTitle("Doctor Profile")
        profile_dialog.setMinimumSize(400, 300)

        layout = QVBoxLayout(profile_dialog)

        # In a real app, we would load the doctor's profile from the database
        layout.addWidget(QLabel("Name: Dr. John Smith"))
        layout.addWidget(QLabel("Specialty: Cardiology"))
        layout.addWidget(QLabel("License: MD12345"))
        layout.addWidget(QLabel("Email: john.smith@medisys.com"))
        layout.addWidget(QLabel("Phone: 555-123-4567"))

        profile_dialog.exec()

    def view_patient_details(self):
        """View details of the selected patient"""
        selected_indexes = self.patients_table.selectedIndexes()
        if not selected_indexes:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Error", "Please select a patient to view.")
            return

        # Get the row of the first selected cell
        row = selected_indexes[0].row()

        # Get patient details
        patient_id = self.patients_model.item(row, 0).text()
        patient_name = self.patients_model.item(row, 1).text()

        # Show patient details dialog
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QTabWidget

        details_dialog = QDialog(self)
        details_dialog.setWindowTitle(f"Patient Details - {patient_name}")
        details_dialog.setMinimumSize(600, 400)

        layout = QVBoxLayout(details_dialog)

        # Patient details tabs
        tabs = QTabWidget()

        # Basic info tab
        basic_info = QWidget()
        basic_layout = QFormLayout(basic_info)
        basic_layout.addRow("Patient ID:", QLabel(patient_id))
        basic_layout.addRow("Name:", QLabel(patient_name))
        basic_layout.addRow("Date of Birth:", QLabel("1978-05-15"))
        basic_layout.addRow("Gender:", QLabel("Male"))
        basic_layout.addRow("Contact:", QLabel("555-123-4567"))
        basic_layout.addRow("Email:", QLabel("john.smith@example.com"))
        basic_layout.addRow("Address:", QLabel("123 Main St, Anytown, USA"))

        # Medical history tab
        medical_history = QWidget()
        medical_layout = QVBoxLayout(medical_history)
        medical_layout.addWidget(QLabel("Medical History:"))

        history_text = QTextEdit()
        history_text.setReadOnly(True)
        history_text.setText("2022-10-15: Annual physical examination\n"
                           "2021-11-20: Diagnosed with hypertension\n"
                           "2020-05-05: Sprained ankle\n"
                           "2019-02-10: Influenza")
        medical_layout.addWidget(history_text)

        # Add tabs
        tabs.addTab(basic_info, "Basic Info")
        tabs.addTab(medical_history, "Medical History")

        layout.addWidget(tabs)

        details_dialog.exec()

    def new_prescription(self):
        """Create a new prescription"""
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QDialogButtonBox

        prescription_dialog = QDialog(self)
        prescription_dialog.setWindowTitle("New Prescription")
        prescription_dialog.setMinimumSize(500, 300)

        layout = QVBoxLayout(prescription_dialog)

        form_layout = QFormLayout()

        patient_combo = QComboBox()
        patient_combo.addItems(["John Smith", "Jane Doe", "Robert Johnson", "Emily Davis", "Michael Brown"])

        medication_input = QLineEdit()
        dosage_input = QLineEdit()
        instructions_input = QTextEdit()

        form_layout.addRow("Patient:", patient_combo)
        form_layout.addRow("Medication:", medication_input)
        form_layout.addRow("Dosage:", dosage_input)
        form_layout.addRow("Instructions:", instructions_input)

        layout.addLayout(form_layout)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(prescription_dialog.accept)
        buttons.rejected.connect(prescription_dialog.reject)

        layout.addWidget(buttons)

        if prescription_dialog.exec() == QDialog.Accepted:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.information(self, "Success", "Prescription created successfully!")
            self.statusBar.showMessage("Prescription created")