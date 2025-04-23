from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, 
                             QTableView, QPushButton, QFormLayout, QLineEdit, QTextEdit,
                             QMessageBox, QDialog, QDialogButtonBox, QComboBox, QDateEdit)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt, QDate

class PatientForm(QDialog):
    def __init__(self, parent=None, patient_data=None):
        super().__init__(parent)
        self.setWindowTitle("Patient Details")
        self.setMinimumWidth(500)
        
        # Create form layout
        layout = QFormLayout(self)
        
        # Create form fields
        self.id_input = QLineEdit()
        self.id_input.setReadOnly(True)
        if patient_data and 'id' in patient_data:
            self.id_input.setText(str(patient_data['id']))
        else:
            self.id_input.setText("Auto-generated")
            
        self.name_input = QLineEdit()
        if patient_data and 'name' in patient_data:
            self.name_input.setText(patient_data['name'])
            
        self.dob_input = QDateEdit()
        self.dob_input.setCalendarPopup(True)
        self.dob_input.setDate(QDate(1980, 1, 1))
        if patient_data and 'dob' in patient_data:
            try:
                year, month, day = map(int, patient_data['dob'].split('-'))
                self.dob_input.setDate(QDate(year, month, day))
            except (ValueError, AttributeError):
                pass
                
        self.gender_input = QComboBox()
        self.gender_input.addItems(["Male", "Female", "Other"])
        if patient_data and 'gender' in patient_data:
            index = self.gender_input.findText(patient_data['gender'])
            if index >= 0:
                self.gender_input.setCurrentIndex(index)
                
        self.contact_input = QLineEdit()
        if patient_data and 'contact' in patient_data:
            self.contact_input.setText(patient_data['contact'])
            
        self.email_input = QLineEdit()
        if patient_data and 'email' in patient_data:
            self.email_input.setText(patient_data['email'])
            
        self.address_input = QTextEdit()
        if patient_data and 'address' in patient_data:
            self.address_input.setText(patient_data['address'])
            
        self.emergency_contact_input = QLineEdit()
        if patient_data and 'emergency_contact' in patient_data:
            self.emergency_contact_input.setText(patient_data['emergency_contact'])
            
        self.insurance_input = QLineEdit()
        if patient_data and 'insurance' in patient_data:
            self.insurance_input.setText(patient_data['insurance'])
        
        # Add fields to form
        layout.addRow("ID:", self.id_input)
        layout.addRow("Name:", self.name_input)
        layout.addRow("Date of Birth:", self.dob_input)
        layout.addRow("Gender:", self.gender_input)
        layout.addRow("Contact:", self.contact_input)
        layout.addRow("Email:", self.email_input)
        layout.addRow("Address:", self.address_input)
        layout.addRow("Emergency Contact:", self.emergency_contact_input)
        layout.addRow("Insurance:", self.insurance_input)
        
        # Add buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addRow(self.button_box)
    
    def get_patient_data(self):
        return {
            'id': self.id_input.text() if self.id_input.text() != "Auto-generated" else None,
            'name': self.name_input.text(),
            'dob': self.dob_input.date().toString("yyyy-MM-dd"),
            'gender': self.gender_input.currentText(),
            'contact': self.contact_input.text(),
            'email': self.email_input.text(),
            'address': self.address_input.toPlainText(),
            'emergency_contact': self.emergency_contact_input.text(),
            'insurance': self.insurance_input.text()
        }

class PatientsWindow(QMainWindow):
    def __init__(self, db=None, user_id=None):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.setWindowTitle("MediSys - Patients Management")
        self.setMinimumSize(1000, 600)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        header_label = QLabel("Patients Management")
        header_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)
        
        # Search bar
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter patient name, ID, or contact")
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_patients)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        
        main_layout.addLayout(search_layout)
        
        # Patients table
        self.patients_table = QTableView()
        self.patients_model = QStandardItemModel(0, 6)
        self.patients_model.setHorizontalHeaderLabels([
            "ID", "Name", "DOB", "Gender", "Contact", "Insurance"
        ])
        self.patients_table.setModel(self.patients_model)
        self.patients_table.setSelectionBehavior(QTableView.SelectRows)
        self.patients_table.setSelectionMode(QTableView.SingleSelection)
        self.patients_table.setEditTriggers(QTableView.NoEditTriggers)
        main_layout.addWidget(self.patients_table)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        self.add_button = QPushButton("Add Patient")
        self.add_button.clicked.connect(self.add_patient)
        buttons_layout.addWidget(self.add_button)
        
        self.edit_button = QPushButton("Edit Patient")
        self.edit_button.clicked.connect(self.edit_patient)
        buttons_layout.addWidget(self.edit_button)
        
        self.delete_button = QPushButton("Delete Patient")
        self.delete_button.clicked.connect(self.delete_patient)
        buttons_layout.addWidget(self.delete_button)
        
        self.view_history_button = QPushButton("View Medical History")
        self.view_history_button.clicked.connect(self.view_medical_history)
        buttons_layout.addWidget(self.view_history_button)
        
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.load_patients)
        buttons_layout.addWidget(self.refresh_button)
        
        main_layout.addLayout(buttons_layout)
        
        # Load patients
        self.load_patients()
    
    def load_patients(self):
        """Load patients from database or use sample data"""
        # Clear existing data
        self.patients_model.removeRows(0, self.patients_model.rowCount())
        
        # In a real application, we would load from the database
        # For now, we'll use sample data
        sample_patients = [
            {
                "id": 1, 
                "name": "John Doe", 
                "dob": "1975-05-15",
                "gender": "Male", 
                "contact": "555-123-4567", 
                "email": "john.doe@example.com",
                "address": "123 Main St, Anytown, USA",
                "emergency_contact": "Jane Doe: 555-987-6543",
                "insurance": "Blue Cross #12345678"
            },
            {
                "id": 2, 
                "name": "Jane Smith", 
                "dob": "1982-08-22",
                "gender": "Female", 
                "contact": "555-234-5678", 
                "email": "jane.smith@example.com",
                "address": "456 Oak Ave, Somewhere, USA",
                "emergency_contact": "John Smith: 555-876-5432",
                "insurance": "Aetna #23456789"
            },
            {
                "id": 3, 
                "name": "Robert Johnson", 
                "dob": "1965-11-30",
                "gender": "Male", 
                "contact": "555-345-6789", 
                "email": "robert.johnson@example.com",
                "address": "789 Pine St, Nowhere, USA",
                "emergency_contact": "Mary Johnson: 555-765-4321",
                "insurance": "Medicare #34567890"
            },
            {
                "id": 4, 
                "name": "Emily Davis", 
                "dob": "1990-02-14",
                "gender": "Female", 
                "contact": "555-456-7890", 
                "email": "emily.davis@example.com",
                "address": "101 Elm St, Elsewhere, USA",
                "emergency_contact": "Michael Davis: 555-654-3210",
                "insurance": "Cigna #45678901"
            },
            {
                "id": 5, 
                "name": "Michael Brown", 
                "dob": "1978-07-04",
                "gender": "Male", 
                "contact": "555-567-8901", 
                "email": "michael.brown@example.com",
                "address": "202 Maple Ave, Anywhere, USA",
                "emergency_contact": "Sarah Brown: 555-543-2109",
                "insurance": "UnitedHealth #56789012"
            }
        ]
        
        # Add patients to the model
        for patient in sample_patients:
            row_items = [
                QStandardItem(str(patient["id"])),
                QStandardItem(patient["name"]),
                QStandardItem(patient["dob"]),
                QStandardItem(patient["gender"]),
                QStandardItem(patient["contact"]),
                QStandardItem(patient["insurance"])
            ]
            self.patients_model.appendRow(row_items)
        
        # Resize columns to content
        self.patients_table.resizeColumnsToContents()
    
    def search_patients(self):
        """Search patients based on input"""
        search_text = self.search_input.text().lower()
        if not search_text:
            self.load_patients()
            return
        
        # Clear existing data
        self.patients_model.removeRows(0, self.patients_model.rowCount())
        
        # In a real application, we would search the database
        # For now, we'll filter our sample data
        sample_patients = [
            {
                "id": 1, 
                "name": "John Doe", 
                "dob": "1975-05-15",
                "gender": "Male", 
                "contact": "555-123-4567", 
                "email": "john.doe@example.com",
                "address": "123 Main St, Anytown, USA",
                "emergency_contact": "Jane Doe: 555-987-6543",
                "insurance": "Blue Cross #12345678"
            },
            {
                "id": 2, 
                "name": "Jane Smith", 
                "dob": "1982-08-22",
                "gender": "Female", 
                "contact": "555-234-5678", 
                "email": "jane.smith@example.com",
                "address": "456 Oak Ave, Somewhere, USA",
                "emergency_contact": "John Smith: 555-876-5432",
                "insurance": "Aetna #23456789"
            },
            {
                "id": 3, 
                "name": "Robert Johnson", 
                "dob": "1965-11-30",
                "gender": "Male", 
                "contact": "555-345-6789", 
                "email": "robert.johnson@example.com",
                "address": "789 Pine St, Nowhere, USA",
                "emergency_contact": "Mary Johnson: 555-765-4321",
                "insurance": "Medicare #34567890"
            },
            {
                "id": 4, 
                "name": "Emily Davis", 
                "dob": "1990-02-14",
                "gender": "Female", 
                "contact": "555-456-7890", 
                "email": "emily.davis@example.com",
                "address": "101 Elm St, Elsewhere, USA",
                "emergency_contact": "Michael Davis: 555-654-3210",
                "insurance": "Cigna #45678901"
            },
            {
                "id": 5, 
                "name": "Michael Brown", 
                "dob": "1978-07-04",
                "gender": "Male", 
                "contact": "555-567-8901", 
                "email": "michael.brown@example.com",
                "address": "202 Maple Ave, Anywhere, USA",
                "emergency_contact": "Sarah Brown: 555-543-2109",
                "insurance": "UnitedHealth #56789012"
            }
        ]
        
        # Filter patients
        filtered_patients = []
        for patient in sample_patients:
            if (search_text in str(patient["id"]).lower() or
                search_text in patient["name"].lower() or
                search_text in patient["contact"].lower() or
                search_text in patient["email"].lower() or
                search_text in patient["insurance"].lower()):
                filtered_patients.append(patient)
        
        # Add filtered patients to the model
        for patient in filtered_patients:
            row_items = [
                QStandardItem(str(patient["id"])),
                QStandardItem(patient["name"]),
                QStandardItem(patient["dob"]),
                QStandardItem(patient["gender"]),
                QStandardItem(patient["contact"]),
                QStandardItem(patient["insurance"])
            ]
            self.patients_model.appendRow(row_items)
        
        # Resize columns to content
        self.patients_table.resizeColumnsToContents()
    
    def add_patient(self):
        """Open dialog to add a new patient"""
        dialog = PatientForm(self)
        if dialog.exec():
            patient_data = dialog.get_patient_data()
            
            # Validate input
            if not patient_data["name"]:
                QMessageBox.warning(self, "Error", "Patient name is required.")
                return
            
            # Generate new ID (in a real app, this would be done by the database)
            new_id = self.patients_model.rowCount() + 1
            
            # Add to model
            row_items = [
                QStandardItem(str(new_id)),
                QStandardItem(patient_data["name"]),
                QStandardItem(patient_data["dob"]),
                QStandardItem(patient_data["gender"]),
                QStandardItem(patient_data["contact"]),
                QStandardItem(patient_data["insurance"])
            ]
            self.patients_model.appendRow(row_items)
            
            QMessageBox.information(self, "Success", f"Patient '{patient_data['name']}' added successfully.")
    
    def edit_patient(self):
        """Open dialog to edit the selected patient"""
        selected_indexes = self.patients_table.selectedIndexes()
        if not selected_indexes:
            QMessageBox.warning(self, "Error", "Please select a patient to edit.")
            return
        
        # Get the row of the first selected cell
        row = selected_indexes[0].row()
        
        # Get patient data from the model
        patient_data = {
            "id": self.patients_model.item(row, 0).text(),
            "name": self.patients_model.item(row, 1).text(),
            "dob": self.patients_model.item(row, 2).text(),
            "gender": self.patients_model.item(row, 3).text(),
            "contact": self.patients_model.item(row, 4).text(),
            "insurance": self.patients_model.item(row, 5).text(),
            "email": "",  # Not shown in the table
            "address": "",  # Not shown in the table
            "emergency_contact": ""  # Not shown in the table
        }
        
        # Open dialog with patient data
        dialog = PatientForm(self, patient_data)
        if dialog.exec():
            updated_data = dialog.get_patient_data()
            
            # Validate input
            if not updated_data["name"]:
                QMessageBox.warning(self, "Error", "Patient name is required.")
                return
            
            # Update model
            self.patients_model.item(row, 1).setText(updated_data["name"])
            self.patients_model.item(row, 2).setText(updated_data["dob"])
            self.patients_model.item(row, 3).setText(updated_data["gender"])
            self.patients_model.item(row, 4).setText(updated_data["contact"])
            self.patients_model.item(row, 5).setText(updated_data["insurance"])
            
            QMessageBox.information(self, "Success", f"Patient '{updated_data['name']}' updated successfully.")
    
    def delete_patient(self):
        """Delete the selected patient"""
        selected_indexes = self.patients_table.selectedIndexes()
        if not selected_indexes:
            QMessageBox.warning(self, "Error", "Please select a patient to delete.")
            return
        
        # Get the row of the first selected cell
        row = selected_indexes[0].row()
        
        # Get patient name
        patient_name = self.patients_model.item(row, 1).text()
        
        # Confirm deletion
        reply = QMessageBox.question(self, "Confirm Deletion", 
                                    f"Are you sure you want to delete patient '{patient_name}'?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Remove from model
            self.patients_model.removeRow(row)
            
            QMessageBox.information(self, "Success", f"Patient '{patient_name}' deleted successfully.")
    
    def view_medical_history(self):
        """View medical history of the selected patient"""
        selected_indexes = self.patients_table.selectedIndexes()
        if not selected_indexes:
            QMessageBox.warning(self, "Error", "Please select a patient to view medical history.")
            return
        
        # Get the row of the first selected cell
        row = selected_indexes[0].row()
        
        # Get patient name
        patient_name = self.patients_model.item(row, 1).text()
        
        # In a real application, we would load the medical history from the database
        # For now, just show a message
        QMessageBox.information(self, "Medical History", 
                               f"Medical history for {patient_name}:\n\n" +
                               "- 2023-05-15: Annual checkup - Dr. Smith\n" +
                               "- 2023-03-22: Flu symptoms - Dr. Johnson\n" +
                               "- 2022-11-10: Sprained ankle - Dr. Williams\n" +
                               "- 2022-08-05: Vaccination - Dr. Brown\n" +
                               "- 2022-04-18: Allergic reaction - Dr. Davis")
