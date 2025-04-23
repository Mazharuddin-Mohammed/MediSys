from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, 
                             QTableView, QPushButton, QFormLayout, QLineEdit, QTextEdit,
                             QMessageBox, QDialog, QDialogButtonBox, QComboBox, QDateEdit,
                             QTimeEdit, QCalendarWidget, QSplitter)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt, QDate, QTime

class AppointmentForm(QDialog):
    def __init__(self, parent=None, appointment_data=None, patients=None, doctors=None):
        super().__init__(parent)
        self.setWindowTitle("Appointment Details")
        self.setMinimumWidth(500)
        
        # Create form layout
        layout = QFormLayout(self)
        
        # Create form fields
        self.id_input = QLineEdit()
        self.id_input.setReadOnly(True)
        if appointment_data and 'id' in appointment_data:
            self.id_input.setText(str(appointment_data['id']))
        else:
            self.id_input.setText("Auto-generated")
            
        self.patient_input = QComboBox()
        if patients:
            self.patient_input.addItems(patients)
        else:
            self.patient_input.addItems(["Patient 1", "Patient 2", "Patient 3", "Patient 4", "Patient 5"])
            
        if appointment_data and 'patient' in appointment_data:
            index = self.patient_input.findText(appointment_data['patient'])
            if index >= 0:
                self.patient_input.setCurrentIndex(index)
                
        self.doctor_input = QComboBox()
        if doctors:
            self.doctor_input.addItems(doctors)
        else:
            self.doctor_input.addItems([
                "John Smith", "Emily Johnson", "Michael Williams", 
                "Sarah Brown", "David Davis"
            ])
            
        if appointment_data and 'doctor' in appointment_data:
            index = self.doctor_input.findText(appointment_data['doctor'])
            if index >= 0:
                self.doctor_input.setCurrentIndex(index)
                
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        if appointment_data and 'date' in appointment_data:
            try:
                year, month, day = map(int, appointment_data['date'].split('-'))
                self.date_input.setDate(QDate(year, month, day))
            except (ValueError, AttributeError):
                pass
                
        self.time_input = QTimeEdit()
        self.time_input.setTime(QTime(9, 0))
        if appointment_data and 'time' in appointment_data:
            try:
                hour, minute = map(int, appointment_data['time'].split(':'))
                self.time_input.setTime(QTime(hour, minute))
            except (ValueError, AttributeError):
                pass
                
        self.duration_input = QComboBox()
        self.duration_input.addItems(["15 minutes", "30 minutes", "45 minutes", "60 minutes"])
        if appointment_data and 'duration' in appointment_data:
            index = self.duration_input.findText(appointment_data['duration'])
            if index >= 0:
                self.duration_input.setCurrentIndex(index)
        else:
            # Default to 30 minutes
            self.duration_input.setCurrentIndex(1)
            
        self.type_input = QComboBox()
        self.type_input.addItems(["Initial Consultation", "Follow-up", "Procedure", "Emergency"])
        if appointment_data and 'type' in appointment_data:
            index = self.type_input.findText(appointment_data['type'])
            if index >= 0:
                self.type_input.setCurrentIndex(index)
                
        self.status_input = QComboBox()
        self.status_input.addItems(["Scheduled", "Confirmed", "Completed", "Cancelled", "No-show"])
        if appointment_data and 'status' in appointment_data:
            index = self.status_input.findText(appointment_data['status'])
            if index >= 0:
                self.status_input.setCurrentIndex(index)
        else:
            # Default to Scheduled
            self.status_input.setCurrentIndex(0)
            
        self.notes_input = QTextEdit()
        if appointment_data and 'notes' in appointment_data:
            self.notes_input.setText(appointment_data['notes'])
        
        # Add fields to form
        layout.addRow("ID:", self.id_input)
        layout.addRow("Patient:", self.patient_input)
        layout.addRow("Doctor:", self.doctor_input)
        layout.addRow("Date:", self.date_input)
        layout.addRow("Time:", self.time_input)
        layout.addRow("Duration:", self.duration_input)
        layout.addRow("Type:", self.type_input)
        layout.addRow("Status:", self.status_input)
        layout.addRow("Notes:", self.notes_input)
        
        # Add buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addRow(self.button_box)
    
    def get_appointment_data(self):
        return {
            'id': self.id_input.text() if self.id_input.text() != "Auto-generated" else None,
            'patient': self.patient_input.currentText(),
            'doctor': self.doctor_input.currentText(),
            'date': self.date_input.date().toString("yyyy-MM-dd"),
            'time': self.time_input.time().toString("HH:mm"),
            'duration': self.duration_input.currentText(),
            'type': self.type_input.currentText(),
            'status': self.status_input.currentText(),
            'notes': self.notes_input.toPlainText()
        }

class AppointmentsWindow(QMainWindow):
    def __init__(self, db=None, user_id=None):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.setWindowTitle("MediSys - Appointments Management")
        self.setMinimumSize(1200, 700)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        header_label = QLabel("Appointments Management")
        header_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)
        
        # Create a splitter for calendar and appointments list
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Calendar widget
        calendar_widget = QWidget()
        calendar_layout = QVBoxLayout(calendar_widget)
        
        calendar_header = QLabel("Appointment Calendar")
        calendar_header.setStyleSheet("font-size: 16px; font-weight: bold;")
        calendar_layout.addWidget(calendar_header)
        
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setMinimumDate(QDate.currentDate().addDays(-365))  # 1 year back
        self.calendar.setMaximumDate(QDate.currentDate().addDays(365))   # 1 year ahead
        self.calendar.clicked.connect(self.date_selected)
        calendar_layout.addWidget(self.calendar)
        
        splitter.addWidget(calendar_widget)
        
        # Appointments list
        appointments_widget = QWidget()
        appointments_layout = QVBoxLayout(appointments_widget)
        
        appointments_header = QLabel("Appointments List")
        appointments_header.setStyleSheet("font-size: 16px; font-weight: bold;")
        appointments_layout.addWidget(appointments_header)
        
        # Filter controls
        filter_layout = QHBoxLayout()
        
        filter_date_label = QLabel("Date:")
        self.filter_date = QDateEdit()
        self.filter_date.setCalendarPopup(True)
        self.filter_date.setDate(QDate.currentDate())
        
        filter_doctor_label = QLabel("Doctor:")
        self.filter_doctor = QComboBox()
        self.filter_doctor.addItem("All Doctors")
        self.filter_doctor.addItems([
            "John Smith", "Emily Johnson", "Michael Williams", 
            "Sarah Brown", "David Davis"
        ])
        
        filter_status_label = QLabel("Status:")
        self.filter_status = QComboBox()
        self.filter_status.addItem("All Statuses")
        self.filter_status.addItems(["Scheduled", "Confirmed", "Completed", "Cancelled", "No-show"])
        
        filter_button = QPushButton("Apply Filter")
        filter_button.clicked.connect(self.apply_filter)
        
        filter_layout.addWidget(filter_date_label)
        filter_layout.addWidget(self.filter_date)
        filter_layout.addWidget(filter_doctor_label)
        filter_layout.addWidget(self.filter_doctor)
        filter_layout.addWidget(filter_status_label)
        filter_layout.addWidget(self.filter_status)
        filter_layout.addWidget(filter_button)
        
        appointments_layout.addLayout(filter_layout)
        
        # Appointments table
        self.appointments_table = QTableView()
        self.appointments_model = QStandardItemModel(0, 8)
        self.appointments_model.setHorizontalHeaderLabels([
            "ID", "Patient", "Doctor", "Date", "Time", "Duration", "Type", "Status"
        ])
        self.appointments_table.setModel(self.appointments_model)
        self.appointments_table.setSelectionBehavior(QTableView.SelectRows)
        self.appointments_table.setSelectionMode(QTableView.SingleSelection)
        self.appointments_table.setEditTriggers(QTableView.NoEditTriggers)
        appointments_layout.addWidget(self.appointments_table)
        
        splitter.addWidget(appointments_widget)
        
        # Set initial splitter sizes
        splitter.setSizes([400, 800])
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        self.add_button = QPushButton("Add Appointment")
        self.add_button.clicked.connect(self.add_appointment)
        buttons_layout.addWidget(self.add_button)
        
        self.edit_button = QPushButton("Edit Appointment")
        self.edit_button.clicked.connect(self.edit_appointment)
        buttons_layout.addWidget(self.edit_button)
        
        self.delete_button = QPushButton("Delete Appointment")
        self.delete_button.clicked.connect(self.delete_appointment)
        buttons_layout.addWidget(self.delete_button)
        
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.load_appointments)
        buttons_layout.addWidget(self.refresh_button)
        
        main_layout.addLayout(buttons_layout)
        
        # Load appointments
        self.load_appointments()
    
    def date_selected(self, date):
        """Handle date selection in calendar"""
        self.filter_date.setDate(date)
        self.apply_filter()
    
    def apply_filter(self):
        """Apply filters to appointments list"""
        self.load_appointments()
    
    def load_appointments(self):
        """Load appointments from database or use sample data"""
        # Clear existing data
        self.appointments_model.removeRows(0, self.appointments_model.rowCount())
        
        # Get filter values
        filter_date = self.filter_date.date().toString("yyyy-MM-dd")
        filter_doctor = self.filter_doctor.currentText()
        filter_status = self.filter_status.currentText()
        
        # In a real application, we would load from the database with filters
        # For now, we'll use sample data
        sample_appointments = [
            {
                "id": 1, 
                "patient": "Patient 1", 
                "doctor": "John Smith",
                "date": "2023-06-15", 
                "time": "09:00", 
                "duration": "30 minutes",
                "type": "Initial Consultation",
                "status": "Completed",
                "notes": "Patient complained of chest pain."
            },
            {
                "id": 2, 
                "patient": "Patient 2", 
                "doctor": "Emily Johnson",
                "date": QDate.currentDate().toString("yyyy-MM-dd"), 
                "time": "10:30", 
                "duration": "45 minutes",
                "type": "Follow-up",
                "status": "Scheduled",
                "notes": "Follow-up for previous neurological symptoms."
            },
            {
                "id": 3, 
                "patient": "Patient 3", 
                "doctor": "Michael Williams",
                "date": QDate.currentDate().toString("yyyy-MM-dd"), 
                "time": "13:15", 
                "duration": "30 minutes",
                "type": "Initial Consultation",
                "status": "Confirmed",
                "notes": "Routine checkup for 5-year-old."
            },
            {
                "id": 4, 
                "patient": "Patient 4", 
                "doctor": "Sarah Brown",
                "date": QDate.currentDate().addDays(1).toString("yyyy-MM-dd"), 
                "time": "11:00", 
                "duration": "60 minutes",
                "type": "Procedure",
                "status": "Scheduled",
                "notes": "Scheduled for knee examination."
            },
            {
                "id": 5, 
                "patient": "Patient 5", 
                "doctor": "David Davis",
                "date": QDate.currentDate().addDays(-1).toString("yyyy-MM-dd"), 
                "time": "14:45", 
                "duration": "45 minutes",
                "type": "Follow-up",
                "status": "Completed",
                "notes": "Follow-up after chemotherapy session."
            }
        ]
        
        # Apply filters
        filtered_appointments = []
        for appt in sample_appointments:
            # Apply date filter
            if filter_date != appt["date"] and filter_date != "":
                continue
                
            # Apply doctor filter
            if filter_doctor != "All Doctors" and filter_doctor != appt["doctor"]:
                continue
                
            # Apply status filter
            if filter_status != "All Statuses" and filter_status != appt["status"]:
                continue
                
            filtered_appointments.append(appt)
        
        # Add appointments to the model
        for appt in filtered_appointments:
            row_items = [
                QStandardItem(str(appt["id"])),
                QStandardItem(appt["patient"]),
                QStandardItem(appt["doctor"]),
                QStandardItem(appt["date"]),
                QStandardItem(appt["time"]),
                QStandardItem(appt["duration"]),
                QStandardItem(appt["type"]),
                QStandardItem(appt["status"])
            ]
            self.appointments_model.appendRow(row_items)
        
        # Resize columns to content
        self.appointments_table.resizeColumnsToContents()
    
    def get_patients(self):
        """Get list of patients (in a real app, this would come from the database)"""
        return ["Patient 1", "Patient 2", "Patient 3", "Patient 4", "Patient 5"]
    
    def get_doctors(self):
        """Get list of doctors (in a real app, this would come from the database)"""
        return ["John Smith", "Emily Johnson", "Michael Williams", "Sarah Brown", "David Davis"]
    
    def add_appointment(self):
        """Open dialog to add a new appointment"""
        dialog = AppointmentForm(self, patients=self.get_patients(), doctors=self.get_doctors())
        if dialog.exec():
            appointment_data = dialog.get_appointment_data()
            
            # Validate input
            if not appointment_data["patient"] or not appointment_data["doctor"]:
                QMessageBox.warning(self, "Error", "Patient and doctor are required.")
                return
            
            # Generate new ID (in a real app, this would be done by the database)
            new_id = self.appointments_model.rowCount() + 1
            
            # Add to model
            row_items = [
                QStandardItem(str(new_id)),
                QStandardItem(appointment_data["patient"]),
                QStandardItem(appointment_data["doctor"]),
                QStandardItem(appointment_data["date"]),
                QStandardItem(appointment_data["time"]),
                QStandardItem(appointment_data["duration"]),
                QStandardItem(appointment_data["type"]),
                QStandardItem(appointment_data["status"])
            ]
            self.appointments_model.appendRow(row_items)
            
            QMessageBox.information(self, "Success", 
                                   f"Appointment for {appointment_data['patient']} with {appointment_data['doctor']} added successfully.")
            
            # Refresh the view
            self.load_appointments()
    
    def edit_appointment(self):
        """Open dialog to edit the selected appointment"""
        selected_indexes = self.appointments_table.selectedIndexes()
        if not selected_indexes:
            QMessageBox.warning(self, "Error", "Please select an appointment to edit.")
            return
        
        # Get the row of the first selected cell
        row = selected_indexes[0].row()
        
        # Get appointment data from the model
        appointment_data = {
            "id": self.appointments_model.item(row, 0).text(),
            "patient": self.appointments_model.item(row, 1).text(),
            "doctor": self.appointments_model.item(row, 2).text(),
            "date": self.appointments_model.item(row, 3).text(),
            "time": self.appointments_model.item(row, 4).text(),
            "duration": self.appointments_model.item(row, 5).text(),
            "type": self.appointments_model.item(row, 6).text(),
            "status": self.appointments_model.item(row, 7).text(),
            "notes": ""  # Notes are not shown in the table
        }
        
        # Open dialog with appointment data
        dialog = AppointmentForm(self, appointment_data, 
                                patients=self.get_patients(), 
                                doctors=self.get_doctors())
        if dialog.exec():
            updated_data = dialog.get_appointment_data()
            
            # Validate input
            if not updated_data["patient"] or not updated_data["doctor"]:
                QMessageBox.warning(self, "Error", "Patient and doctor are required.")
                return
            
            # Update model
            self.appointments_model.item(row, 1).setText(updated_data["patient"])
            self.appointments_model.item(row, 2).setText(updated_data["doctor"])
            self.appointments_model.item(row, 3).setText(updated_data["date"])
            self.appointments_model.item(row, 4).setText(updated_data["time"])
            self.appointments_model.item(row, 5).setText(updated_data["duration"])
            self.appointments_model.item(row, 6).setText(updated_data["type"])
            self.appointments_model.item(row, 7).setText(updated_data["status"])
            
            QMessageBox.information(self, "Success", 
                                   f"Appointment for {updated_data['patient']} with {updated_data['doctor']} updated successfully.")
            
            # Refresh the view
            self.load_appointments()
    
    def delete_appointment(self):
        """Delete the selected appointment"""
        selected_indexes = self.appointments_table.selectedIndexes()
        if not selected_indexes:
            QMessageBox.warning(self, "Error", "Please select an appointment to delete.")
            return
        
        # Get the row of the first selected cell
        row = selected_indexes[0].row()
        
        # Get appointment details
        patient = self.appointments_model.item(row, 1).text()
        doctor = self.appointments_model.item(row, 2).text()
        date = self.appointments_model.item(row, 3).text()
        time = self.appointments_model.item(row, 4).text()
        
        # Confirm deletion
        reply = QMessageBox.question(self, "Confirm Deletion", 
                                    f"Are you sure you want to delete the appointment for {patient} with {doctor} on {date} at {time}?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Remove from model
            self.appointments_model.removeRow(row)
            
            QMessageBox.information(self, "Success", "Appointment deleted successfully.")
            
            # Refresh the view
            self.load_appointments()
