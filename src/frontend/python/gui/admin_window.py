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

        # Patients tab
        patients_widget = QWidget()
        patients_layout = QVBoxLayout(patients_widget)

        # Patient search
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        search_input = QLineEdit()
        search_button = QPushButton("Search")
        search_layout.addWidget(search_label)
        search_layout.addWidget(search_input)
        search_layout.addWidget(search_button)
        patients_layout.addLayout(search_layout)

        # Patient list
        patients_table = QTableView()
        patients_model = QStandardItemModel(0, 5)
        patients_model.setHorizontalHeaderLabels(["ID", "Name", "DOB", "Gender", "Contact"])
        patients_table.setModel(patients_model)
        patients_layout.addWidget(patients_table)

        # Patient actions
        actions_layout = QHBoxLayout()
        add_patient_button = QPushButton("Add Patient")
        add_patient_button.clicked.connect(self.show_add_patient_form)
        edit_patient_button = QPushButton("Edit Patient")
        edit_patient_button.clicked.connect(self.show_edit_patient_form)
        delete_patient_button = QPushButton("Delete Patient")
        delete_patient_button.clicked.connect(self.delete_patient)
        actions_layout.addWidget(add_patient_button)
        actions_layout.addWidget(edit_patient_button)
        actions_layout.addWidget(delete_patient_button)
        patients_layout.addLayout(actions_layout)

        # Patient form (hidden by default)
        self.patient_form = QWidget()
        self.patient_form.setVisible(False)
        form_layout = QFormLayout(self.patient_form)

        self.patient_id_input = QLineEdit()
        self.patient_id_input.setReadOnly(True)
        self.patient_id_input.setPlaceholderText("Auto-generated")

        self.patient_name_input = QLineEdit()
        self.patient_dob_input = QDateEdit()
        self.patient_dob_input.setCalendarPopup(True)
        self.patient_dob_input.setDate(QDate(1980, 1, 1))

        self.patient_gender_input = QComboBox()
        self.patient_gender_input.addItems(["Male", "Female", "Other"])

        self.patient_contact_input = QLineEdit()
        self.patient_address_input = QTextEdit()

        form_layout.addRow("ID:", self.patient_id_input)
        form_layout.addRow("Name:", self.patient_name_input)
        form_layout.addRow("Date of Birth:", self.patient_dob_input)
        form_layout.addRow("Gender:", self.patient_gender_input)
        form_layout.addRow("Contact:", self.patient_contact_input)
        form_layout.addRow("Address:", self.patient_address_input)

        form_buttons_layout = QHBoxLayout()
        self.save_patient_button = QPushButton("Save")
        self.save_patient_button.clicked.connect(self.save_patient)
        self.cancel_patient_button = QPushButton("Cancel")
        self.cancel_patient_button.clicked.connect(self.hide_patient_form)
        form_buttons_layout.addWidget(self.save_patient_button)
        form_buttons_layout.addWidget(self.cancel_patient_button)
        form_layout.addRow("", form_buttons_layout)

        patients_layout.addWidget(self.patient_form)

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
        self.tabs.addTab(patients_widget, "Patients")
        self.tabs.addTab(audit_widget, "Audit Log")

        # Add some sample data
        self.add_sample_data()

    def add_sample_data(self):
        """Add sample data to the tables for demonstration purposes"""
        # Add sample patients
        patients_table = None
        for table in self.findChildren(QTableView):
            if table.parent() and isinstance(table.parent(), QWidget) and table.parent().layout() and isinstance(table.parent().layout(), QVBoxLayout):
                # Check if this table is in the patients tab
                if self.tabs.indexOf(table.parent()) == 1:  # Patients tab index
                    patients_table = table
                    break

        if patients_table and patients_table.model():
            patients_model = patients_table.model()
            for i in range(5):
                row_items = [
                    QStandardItem(str(i+1)),
                    QStandardItem(f"Patient {i+1}"),
                    QStandardItem(f"1980-01-{i+1}"),
                    QStandardItem("Male" if i % 2 == 0 else "Female"),
                    QStandardItem(f"555-123-{1000+i}")
                ]
                patients_model.appendRow(row_items)

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
        self.tabs.setCurrentIndex(1)  # Switch to Patients tab
        self.statusBar.showMessage("Viewing patients")

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

    def show_add_patient_form(self):
        # Clear form fields
        self.patient_id_input.clear()
        self.patient_name_input.clear()
        self.patient_dob_input.setDate(QDate(1980, 1, 1))
        self.patient_gender_input.setCurrentIndex(0)
        self.patient_contact_input.clear()
        self.patient_address_input.clear()

        # Show the form
        self.patient_form.setVisible(True)
        self.statusBar.showMessage("Adding new patient")

    def show_edit_patient_form(self):
        # Get the selected patient from the table
        patients_table = None
        for table in self.findChildren(QTableView):
            if table.parent() and isinstance(table.parent(), QWidget) and table.parent().layout() and isinstance(table.parent().layout(), QVBoxLayout):
                if self.tabs.indexOf(table.parent()) == 1:  # Patients tab index
                    patients_table = table
                    break

        if not patients_table:
            QMessageBox.warning(self, "Error", "Could not find patients table.")
            return

        selected_indexes = patients_table.selectedIndexes()
        if not selected_indexes:
            QMessageBox.warning(self, "Error", "Please select a patient to edit.")
            return

        # Get the row of the first selected cell
        row = selected_indexes[0].row()
        model = patients_table.model()

        # Fill the form with the selected patient's data
        self.patient_id_input.setText(model.item(row, 0).text())
        self.patient_name_input.setText(model.item(row, 1).text())

        # Parse the date
        dob_text = model.item(row, 2).text()
        try:
            year, month, day = map(int, dob_text.split('-'))
            self.patient_dob_input.setDate(QDate(year, month, day))
        except (ValueError, AttributeError):
            self.patient_dob_input.setDate(QDate(1980, 1, 1))

        # Set gender
        gender_text = model.item(row, 3).text()
        gender_index = 0  # Default to Male
        if gender_text == "Female":
            gender_index = 1
        elif gender_text == "Other":
            gender_index = 2
        self.patient_gender_input.setCurrentIndex(gender_index)

        # Set contact
        self.patient_contact_input.setText(model.item(row, 4).text())

        # Address is not shown in the table, so we'll leave it empty
        self.patient_address_input.clear()

        # Show the form
        self.patient_form.setVisible(True)
        self.statusBar.showMessage("Editing patient")

    def hide_patient_form(self):
        self.patient_form.setVisible(False)
        self.statusBar.showMessage("Ready")

    def save_patient(self):
        # Get values from form
        patient_id = self.patient_id_input.text()
        name = self.patient_name_input.text()
        dob = self.patient_dob_input.date().toString("yyyy-MM-dd")
        gender = self.patient_gender_input.currentText()
        contact = self.patient_contact_input.text()
        address = self.patient_address_input.toPlainText()

        # Validate input
        if not name:
            QMessageBox.warning(self, "Error", "Name is required.")
            return

        # Get the patients table
        patients_table = None
        for table in self.findChildren(QTableView):
            if table.parent() and isinstance(table.parent(), QWidget) and table.parent().layout() and isinstance(table.parent().layout(), QVBoxLayout):
                if self.tabs.indexOf(table.parent()) == 1:  # Patients tab index
                    patients_table = table
                    break

        if not patients_table:
            QMessageBox.warning(self, "Error", "Could not find patients table.")
            return

        model = patients_table.model()

        # If patient_id is empty, add a new patient
        if not patient_id:
            # Generate a new ID
            new_id = model.rowCount() + 1

            # Add a new row to the table
            model.appendRow([
                QStandardItem(str(new_id)),
                QStandardItem(name),
                QStandardItem(dob),
                QStandardItem(gender),
                QStandardItem(contact)
            ])

            QMessageBox.information(self, "Success", f"Patient {name} added successfully.")
        else:
            # Find the row with the matching ID
            row = -1
            for i in range(model.rowCount()):
                if model.item(i, 0).text() == patient_id:
                    row = i
                    break

            if row == -1:
                QMessageBox.warning(self, "Error", f"Could not find patient with ID {patient_id}.")
                return

            # Update the row
            model.item(row, 1).setText(name)
            model.item(row, 2).setText(dob)
            model.item(row, 3).setText(gender)
            model.item(row, 4).setText(contact)

            QMessageBox.information(self, "Success", f"Patient {name} updated successfully.")

        # Hide the form
        self.hide_patient_form()

    def delete_patient(self):
        # Get the selected patient from the table
        patients_table = None
        for table in self.findChildren(QTableView):
            if table.parent() and isinstance(table.parent(), QWidget) and table.parent().layout() and isinstance(table.parent().layout(), QVBoxLayout):
                if self.tabs.indexOf(table.parent()) == 1:  # Patients tab index
                    patients_table = table
                    break

        if not patients_table:
            QMessageBox.warning(self, "Error", "Could not find patients table.")
            return

        selected_indexes = patients_table.selectedIndexes()
        if not selected_indexes:
            QMessageBox.warning(self, "Error", "Please select a patient to delete.")
            return

        # Get the row of the first selected cell
        row = selected_indexes[0].row()
        model = patients_table.model()

        # Get patient details
        patient_id = model.item(row, 0).text()
        patient_name = model.item(row, 1).text()

        # Confirm deletion
        reply = QMessageBox.question(self, "Confirm Deletion",
                                    f"Are you sure you want to delete patient {patient_name}?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # Remove the row
            model.removeRow(row)
            QMessageBox.information(self, "Success", f"Patient {patient_name} deleted successfully.")
            self.statusBar.showMessage(f"Deleted patient {patient_id}")