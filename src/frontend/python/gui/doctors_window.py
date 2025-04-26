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
                             QMessageBox, QDialog, QDialogButtonBox, QComboBox, QDateEdit,
                             QFileDialog)
from PySide6.QtGui import QStandardItemModel, QStandardItem, QPixmap, QImage
from PySide6.QtCore import Qt, QDate, QSize, QBuffer, QIODevice, QByteArray
import os
import base64

class DoctorForm(QDialog):
    def __init__(self, parent=None, doctor_data=None, departments=None):
        super().__init__(parent)
        self.setWindowTitle("Doctor Details")
        self.setMinimumWidth(600)

        # Main layout
        main_layout = QHBoxLayout(self)

        # Photo section (left side)
        photo_widget = QWidget()
        photo_layout = QVBoxLayout(photo_widget)

        # Photo display
        self.photo_label = QLabel()
        self.photo_label.setFixedSize(200, 200)
        self.photo_label.setAlignment(Qt.AlignCenter)
        self.photo_label.setStyleSheet("border: 1px solid #CCCCCC;")

        # Initialize with placeholder image
        self.photo_data = None
        if doctor_data and 'photo' in doctor_data and doctor_data['photo']:
            # If photo data is provided, use it
            self.photo_data = doctor_data['photo']
            pixmap = QPixmap()
            pixmap.loadFromData(base64.b64decode(self.photo_data))
            self.photo_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            # Use placeholder image
            placeholder_path = "src/frontend/python/resources/images/placeholders/doctor_placeholder.png"
            if os.path.exists(placeholder_path):
                pixmap = QPixmap(placeholder_path)
                self.photo_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                self.photo_label.setText("No Photo")

        photo_layout.addWidget(self.photo_label)

        # Photo buttons
        photo_buttons_layout = QHBoxLayout()

        self.upload_photo_button = QPushButton("Upload Photo")
        self.upload_photo_button.clicked.connect(self.upload_photo)

        self.remove_photo_button = QPushButton("Remove Photo")
        self.remove_photo_button.clicked.connect(self.remove_photo)

        photo_buttons_layout.addWidget(self.upload_photo_button)
        photo_buttons_layout.addWidget(self.remove_photo_button)

        photo_layout.addLayout(photo_buttons_layout)
        photo_layout.addStretch()

        main_layout.addWidget(photo_widget)

        # Form section (right side)
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)

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
        form_layout.addRow("ID:", self.id_input)
        form_layout.addRow("First Name:", self.first_name_input)
        form_layout.addRow("Last Name:", self.last_name_input)
        form_layout.addRow("Specialization:", self.specialization_input)
        form_layout.addRow("License Number:", self.license_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Phone:", self.phone_input)
        form_layout.addRow("Department:", self.department_input)
        form_layout.addRow("Hire Date:", self.hire_date_input)

        # Add buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        form_layout.addRow(self.button_box)

        main_layout.addWidget(form_widget)

        # Set the ratio between photo and form sections
        main_layout.setStretch(0, 1)  # Photo section
        main_layout.setStretch(1, 2)  # Form section

    def upload_photo(self):
        """Open file dialog to select a photo"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Photo", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )

        if file_path:
            # Load the selected image
            pixmap = QPixmap(file_path)

            # Scale the image to fit the label while maintaining aspect ratio
            self.photo_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))

            # Convert the image to base64 for storage
            image = QImage(file_path)
            byte_array = QByteArray()
            buffer = QBuffer(byte_array)
            buffer.open(QIODevice.WriteOnly)
            image.save(buffer, "PNG")
            self.photo_data = base64.b64encode(byte_array.data()).decode('utf-8')

    def remove_photo(self):
        """Remove the current photo and use placeholder"""
        self.photo_data = None
        placeholder_path = "src/frontend/python/resources/images/placeholders/doctor_placeholder.png"
        if os.path.exists(placeholder_path):
            pixmap = QPixmap(placeholder_path)
            self.photo_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.photo_label.clear()
            self.photo_label.setText("No Photo")

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
            'hire_date': self.hire_date_input.date().toString("yyyy-MM-dd"),
            'photo': self.photo_data
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
        self.doctors_model = QStandardItemModel(0, 9)  # Added column for photo indicator
        self.doctors_model.setHorizontalHeaderLabels([
            "Photo", "ID", "Name", "Specialization", "License", "Email", "Phone", "Department", "Hire Date"
        ])
        self.doctors_table.setModel(self.doctors_model)
        self.doctors_table.setSelectionBehavior(QTableView.SelectRows)
        self.doctors_table.setSelectionMode(QTableView.SingleSelection)
        self.doctors_table.setEditTriggers(QTableView.NoEditTriggers)
        self.doctors_table.setColumnWidth(0, 60)  # Photo column width
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
                "hire_date": "2018-05-15",
                "photo": None  # No photo
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
                "hire_date": "2019-03-22",
                "photo": None  # No photo
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
                "hire_date": "2017-11-10",
                "photo": None  # No photo
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
                "hire_date": "2020-01-05",
                "photo": None  # No photo
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
                "hire_date": "2016-08-30",
                "photo": None  # No photo
            }
        ]

        # Add doctors to the model
        for doc in sample_doctors:
            # Create photo status item
            photo_item = QStandardItem()
            if doc.get("photo"):
                photo_item.setText("Yes")
            else:
                photo_item.setText("No")
            photo_item.setTextAlignment(Qt.AlignCenter)

            row_items = [
                photo_item,
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

            # Create photo status item
            photo_item = QStandardItem()
            if doctor_data.get("photo"):
                photo_item.setText("Yes")
            else:
                photo_item.setText("No")
            photo_item.setTextAlignment(Qt.AlignCenter)

            # Add to model
            row_items = [
                photo_item,
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
        name_parts = self.doctors_model.item(row, 2).text().split()  # Name is now in column 2
        first_name = name_parts[0] if name_parts else ""
        last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

        doctor_data = {
            "id": self.doctors_model.item(row, 1).text(),  # ID is now in column 1
            "first_name": first_name,
            "last_name": last_name,
            "specialization": self.doctors_model.item(row, 3).text(),
            "license": self.doctors_model.item(row, 4).text(),
            "email": self.doctors_model.item(row, 5).text(),
            "phone": self.doctors_model.item(row, 6).text(),
            "department": self.doctors_model.item(row, 7).text(),
            "hire_date": self.doctors_model.item(row, 8).text(),
            "photo": None  # Will be updated if available
        }

        # Check if this doctor has a photo (based on the "Yes" indicator)
        has_photo = self.doctors_model.item(row, 0).text() == "Yes"

        # In a real application, we would retrieve the photo data from the database
        # For now, we'll just set a flag to indicate whether a photo exists

        # Open dialog with doctor data
        dialog = DoctorForm(self, doctor_data, departments=self.get_departments())
        if dialog.exec():
            updated_data = dialog.get_doctor_data()

            # Validate input
            if not updated_data["first_name"] or not updated_data["last_name"]:
                QMessageBox.warning(self, "Error", "First name and last name are required.")
                return

            # Update photo status
            if updated_data.get("photo"):
                self.doctors_model.item(row, 0).setText("Yes")
            else:
                self.doctors_model.item(row, 0).setText("No")

            # Update model
            self.doctors_model.item(row, 2).setText(f"{updated_data['first_name']} {updated_data['last_name']}")
            self.doctors_model.item(row, 3).setText(updated_data["specialization"])
            self.doctors_model.item(row, 4).setText(updated_data["license"])
            self.doctors_model.item(row, 5).setText(updated_data["email"])
            self.doctors_model.item(row, 6).setText(updated_data["phone"])
            self.doctors_model.item(row, 7).setText(updated_data["department"])
            self.doctors_model.item(row, 8).setText(updated_data["hire_date"])

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
        doctor_name = self.doctors_model.item(row, 2).text()

        # Confirm deletion
        reply = QMessageBox.question(self, "Confirm Deletion",
                                    f"Are you sure you want to delete doctor '{doctor_name}'?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # Remove from model
            self.doctors_model.removeRow(row)

            QMessageBox.information(self, "Success", f"Doctor '{doctor_name}' deleted successfully.")
