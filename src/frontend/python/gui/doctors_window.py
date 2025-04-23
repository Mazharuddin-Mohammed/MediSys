"""
Doctors Window Module for MediSys Hospital Management System

This module implements the dedicated window for doctor management, including
functionality for adding, editing, and deleting doctor records. It allows
tracking of doctor information such as specialization, license, contact details,
and department assignment.

Author: Mazharuddin Mohammed
"""

from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel,
                             QTableView, QPushButton, QFormLayout, QLineEdit, QTextEdit,
                             QMessageBox, QDialog, QDialogButtonBox, QComboBox, QDateEdit)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt, QDate

class DoctorForm(QDialog):
    def __init__(self, parent=None, doctor_data=None, departments=None):
        super().__init__(parent)
        self.setWindowTitle("Doctor Details")
        self.setMinimumWidth(500)

        # Create form layout
        layout = QFormLayout(self)

        # Create form fields
        self.id_input = QLineEdit()
        self.id_input.setReadOnly(True)
        if doctor_data and 'id' in doctor_data:
            self.id_input.setText(str(doctor_data['id']))
        else:
            self.id_input.setText("Auto-generated")

        self.first_name_input = QLineEdit()
        if doctor_data and 'first_name' in doctor_data:
            self.first_name_input.setText(doctor_data['first_name'])

        self.last_name_input = QLineEdit()
        if doctor_data and 'last_name' in doctor_data:
            self.last_name_input.setText(doctor_data['last_name'])

        self.specialization_input = QLineEdit()
        if doctor_data and 'specialization' in doctor_data:
            self.specialization_input.setText(doctor_data['specialization'])

        self.license_input = QLineEdit()
        if doctor_data and 'license' in doctor_data:
            self.license_input.setText(doctor_data['license'])

        self.email_input = QLineEdit()
        if doctor_data and 'email' in doctor_data:
            self.email_input.setText(doctor_data['email'])

        self.phone_input = QLineEdit()
        if doctor_data and 'phone' in doctor_data:
            self.phone_input.setText(doctor_data['phone'])

        self.department_input = QComboBox()
        if departments:
            self.department_input.addItems(departments)
        else:
            self.department_input.addItems(["Cardiology", "Neurology", "Pediatrics", "Orthopedics", "Oncology"])

        if doctor_data and 'department' in doctor_data:
            index = self.department_input.findText(doctor_data['department'])
            if index >= 0:
                self.department_input.setCurrentIndex(index)

        self.hire_date_input = QDateEdit()
        self.hire_date_input.setCalendarPopup(True)
        self.hire_date_input.setDate(QDate.currentDate())
        if doctor_data and 'hire_date' in doctor_data:
            try:
                year, month, day = map(int, doctor_data['hire_date'].split('-'))
                self.hire_date_input.setDate(QDate(year, month, day))
            except (ValueError, AttributeError):
                pass

        # Add fields to form
        layout.addRow("ID:", self.id_input)
        layout.addRow("First Name:", self.first_name_input)
        layout.addRow("Last Name:", self.last_name_input)
        layout.addRow("Specialization:", self.specialization_input)
        layout.addRow("License Number:", self.license_input)
        layout.addRow("Email:", self.email_input)
        layout.addRow("Phone:", self.phone_input)
        layout.addRow("Department:", self.department_input)
        layout.addRow("Hire Date:", self.hire_date_input)

        # Add buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addRow(self.button_box)

    def get_doctor_data(self):
        return {
            'id': self.id_input.text() if self.id_input.text() != "Auto-generated" else None,
            'first_name': self.first_name_input.text(),
            'last_name': self.last_name_input.text(),
            'specialization': self.specialization_input.text(),
            'license': self.license_input.text(),
            'email': self.email_input.text(),
            'phone': self.phone_input.text(),
            'department': self.department_input.currentText(),
            'hire_date': self.hire_date_input.date().toString("yyyy-MM-dd")
        }

class DoctorsWindow(QMainWindow):
    def __init__(self, db=None, user_id=None):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.setWindowTitle("MediSys - Doctors Management")
        self.setMinimumSize(1000, 600)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Header
        header_label = QLabel("Doctors Management")
        header_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)

        # Doctors list
        self.doctors_table = QTableView()
        self.doctors_model = QStandardItemModel(0, 8)
        self.doctors_model.setHorizontalHeaderLabels([
            "ID", "Name", "Specialization", "License", "Email", "Phone", "Department", "Hire Date"
        ])
        self.doctors_table.setModel(self.doctors_model)
        self.doctors_table.setSelectionBehavior(QTableView.SelectRows)
        self.doctors_table.setSelectionMode(QTableView.SingleSelection)
        self.doctors_table.setEditTriggers(QTableView.NoEditTriggers)
        main_layout.addWidget(self.doctors_table)

        # Buttons
        buttons_layout = QHBoxLayout()

        self.add_button = QPushButton("Add Doctor")
        self.add_button.clicked.connect(self.add_doctor)
        buttons_layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Edit Doctor")
        self.edit_button.clicked.connect(self.edit_doctor)
        buttons_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Delete Doctor")
        self.delete_button.clicked.connect(self.delete_doctor)
        buttons_layout.addWidget(self.delete_button)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.load_doctors)
        buttons_layout.addWidget(self.refresh_button)

        main_layout.addLayout(buttons_layout)

        # Load doctors
        self.load_doctors()

    def load_doctors(self):
        """Load doctors from database or use sample data"""
        # Clear existing data
        self.doctors_model.removeRows(0, self.doctors_model.rowCount())

        # In a real application, we would load from the database
        # For now, we'll use sample data
        sample_doctors = [
            {
                "id": 1,
                "first_name": "John",
                "last_name": "Smith",
                "specialization": "Cardiology",
                "license": "MD12345",
                "email": "john.smith@medisys.com",
                "phone": "555-123-4567",
                "department": "Cardiology",
                "hire_date": "2018-05-15"
            },
            {
                "id": 2,
                "first_name": "Emily",
                "last_name": "Johnson",
                "specialization": "Neurology",
                "license": "MD23456",
                "email": "emily.johnson@medisys.com",
                "phone": "555-234-5678",
                "department": "Neurology",
                "hire_date": "2019-03-22"
            },
            {
                "id": 3,
                "first_name": "Michael",
                "last_name": "Williams",
                "specialization": "Pediatrics",
                "license": "MD34567",
                "email": "michael.williams@medisys.com",
                "phone": "555-345-6789",
                "department": "Pediatrics",
                "hire_date": "2017-11-10"
            },
            {
                "id": 4,
                "first_name": "Sarah",
                "last_name": "Brown",
                "specialization": "Orthopedics",
                "license": "MD45678",
                "email": "sarah.brown@medisys.com",
                "phone": "555-456-7890",
                "department": "Orthopedics",
                "hire_date": "2020-01-05"
            },
            {
                "id": 5,
                "first_name": "David",
                "last_name": "Davis",
                "specialization": "Oncology",
                "license": "MD56789",
                "email": "david.davis@medisys.com",
                "phone": "555-567-8901",
                "department": "Oncology",
                "hire_date": "2016-08-30"
            }
        ]

        # Add doctors to the model
        for doc in sample_doctors:
            row_items = [
                QStandardItem(str(doc["id"])),
                QStandardItem(f"{doc['first_name']} {doc['last_name']}"),
                QStandardItem(doc["specialization"]),
                QStandardItem(doc["license"]),
                QStandardItem(doc["email"]),
                QStandardItem(doc["phone"]),
                QStandardItem(doc["department"]),
                QStandardItem(doc["hire_date"])
            ]
            self.doctors_model.appendRow(row_items)

        # Resize columns to content
        self.doctors_table.resizeColumnsToContents()

    def get_departments(self):
        """Get list of departments (in a real app, this would come from the database)"""
        return ["Cardiology", "Neurology", "Pediatrics", "Orthopedics", "Oncology"]

    def add_doctor(self):
        """Open dialog to add a new doctor"""
        dialog = DoctorForm(self, departments=self.get_departments())
        if dialog.exec():
            doctor_data = dialog.get_doctor_data()

            # Validate input
            if not doctor_data["first_name"] or not doctor_data["last_name"]:
                QMessageBox.warning(self, "Error", "First name and last name are required.")
                return

            # Generate new ID (in a real app, this would be done by the database)
            new_id = self.doctors_model.rowCount() + 1

            # Add to model
            row_items = [
                QStandardItem(str(new_id)),
                QStandardItem(f"{doctor_data['first_name']} {doctor_data['last_name']}"),
                QStandardItem(doctor_data["specialization"]),
                QStandardItem(doctor_data["license"]),
                QStandardItem(doctor_data["email"]),
                QStandardItem(doctor_data["phone"]),
                QStandardItem(doctor_data["department"]),
                QStandardItem(doctor_data["hire_date"])
            ]
            self.doctors_model.appendRow(row_items)

            QMessageBox.information(self, "Success",
                                   f"Doctor '{doctor_data['first_name']} {doctor_data['last_name']}' added successfully.")

    def edit_doctor(self):
        """Open dialog to edit the selected doctor"""
        selected_indexes = self.doctors_table.selectedIndexes()
        if not selected_indexes:
            QMessageBox.warning(self, "Error", "Please select a doctor to edit.")
            return

        # Get the row of the first selected cell
        row = selected_indexes[0].row()

        # Get doctor data from the model
        name_parts = self.doctors_model.item(row, 1).text().split()
        first_name = name_parts[0] if name_parts else ""
        last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

        doctor_data = {
            "id": self.doctors_model.item(row, 0).text(),
            "first_name": first_name,
            "last_name": last_name,
            "specialization": self.doctors_model.item(row, 2).text(),
            "license": self.doctors_model.item(row, 3).text(),
            "email": self.doctors_model.item(row, 4).text(),
            "phone": self.doctors_model.item(row, 5).text(),
            "department": self.doctors_model.item(row, 6).text(),
            "hire_date": self.doctors_model.item(row, 7).text()
        }

        # Open dialog with doctor data
        dialog = DoctorForm(self, doctor_data, departments=self.get_departments())
        if dialog.exec():
            updated_data = dialog.get_doctor_data()

            # Validate input
            if not updated_data["first_name"] or not updated_data["last_name"]:
                QMessageBox.warning(self, "Error", "First name and last name are required.")
                return

            # Update model
            self.doctors_model.item(row, 1).setText(f"{updated_data['first_name']} {updated_data['last_name']}")
            self.doctors_model.item(row, 2).setText(updated_data["specialization"])
            self.doctors_model.item(row, 3).setText(updated_data["license"])
            self.doctors_model.item(row, 4).setText(updated_data["email"])
            self.doctors_model.item(row, 5).setText(updated_data["phone"])
            self.doctors_model.item(row, 6).setText(updated_data["department"])
            self.doctors_model.item(row, 7).setText(updated_data["hire_date"])

            QMessageBox.information(self, "Success",
                                   f"Doctor '{updated_data['first_name']} {updated_data['last_name']}' updated successfully.")

    def delete_doctor(self):
        """Delete the selected doctor"""
        selected_indexes = self.doctors_table.selectedIndexes()
        if not selected_indexes:
            QMessageBox.warning(self, "Error", "Please select a doctor to delete.")
            return

        # Get the row of the first selected cell
        row = selected_indexes[0].row()

        # Get doctor name
        doctor_name = self.doctors_model.item(row, 1).text()

        # Confirm deletion
        reply = QMessageBox.question(self, "Confirm Deletion",
                                    f"Are you sure you want to delete doctor '{doctor_name}'?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # Remove from model
            self.doctors_model.removeRow(row)

            QMessageBox.information(self, "Success", f"Doctor '{doctor_name}' deleted successfully.")
