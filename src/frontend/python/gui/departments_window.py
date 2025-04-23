"""
Departments Window Module for MediSys Hospital Management System

This module implements the dedicated window for department management, including
functionality for adding, editing, and deleting department records. It allows
tracking of department information such as name, description, location, and head.

Author: Mazharuddin Mohammed
"""

from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel,
                             QTableView, QPushButton, QFormLayout, QLineEdit, QTextEdit,
                             QMessageBox, QDialog, QDialogButtonBox)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt

class DepartmentForm(QDialog):
    def __init__(self, parent=None, department_data=None):
        super().__init__(parent)
        self.setWindowTitle("Department Details")
        self.setMinimumWidth(400)

        # Create form layout
        layout = QFormLayout(self)

        # Create form fields
        self.id_input = QLineEdit()
        self.id_input.setReadOnly(True)
        if department_data and 'id' in department_data:
            self.id_input.setText(str(department_data['id']))
        else:
            self.id_input.setText("Auto-generated")

        self.name_input = QLineEdit()
        if department_data and 'name' in department_data:
            self.name_input.setText(department_data['name'])

        self.description_input = QTextEdit()
        if department_data and 'description' in department_data:
            self.description_input.setText(department_data['description'])

        self.location_input = QLineEdit()
        if department_data and 'location' in department_data:
            self.location_input.setText(department_data['location'])

        self.head_input = QLineEdit()
        if department_data and 'head' in department_data:
            self.head_input.setText(department_data['head'])

        # Add fields to form
        layout.addRow("ID:", self.id_input)
        layout.addRow("Name:", self.name_input)
        layout.addRow("Description:", self.description_input)
        layout.addRow("Location:", self.location_input)
        layout.addRow("Department Head:", self.head_input)

        # Add buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addRow(self.button_box)

    def get_department_data(self):
        return {
            'id': self.id_input.text() if self.id_input.text() != "Auto-generated" else None,
            'name': self.name_input.text(),
            'description': self.description_input.toPlainText(),
            'location': self.location_input.text(),
            'head': self.head_input.text()
        }

class DepartmentsWindow(QMainWindow):
    def __init__(self, db=None, user_id=None):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.setWindowTitle("MediSys - Departments Management")
        self.setMinimumSize(800, 600)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Header
        header_label = QLabel("Departments Management")
        header_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)

        # Department list
        self.departments_table = QTableView()
        self.departments_model = QStandardItemModel(0, 5)
        self.departments_model.setHorizontalHeaderLabels(["ID", "Name", "Description", "Location", "Department Head"])
        self.departments_table.setModel(self.departments_model)
        self.departments_table.setSelectionBehavior(QTableView.SelectRows)
        self.departments_table.setSelectionMode(QTableView.SingleSelection)
        self.departments_table.setEditTriggers(QTableView.NoEditTriggers)
        main_layout.addWidget(self.departments_table)

        # Buttons
        buttons_layout = QHBoxLayout()

        self.add_button = QPushButton("Add Department")
        self.add_button.clicked.connect(self.add_department)
        buttons_layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Edit Department")
        self.edit_button.clicked.connect(self.edit_department)
        buttons_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Delete Department")
        self.delete_button.clicked.connect(self.delete_department)
        buttons_layout.addWidget(self.delete_button)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.load_departments)
        buttons_layout.addWidget(self.refresh_button)

        main_layout.addLayout(buttons_layout)

        # Load departments
        self.load_departments()

    def load_departments(self):
        """Load departments from database or use sample data"""
        # Clear existing data
        self.departments_model.removeRows(0, self.departments_model.rowCount())

        # In a real application, we would load from the database
        # For now, we'll use sample data
        sample_departments = [
            {"id": 1, "name": "Cardiology", "description": "Heart and cardiovascular system",
             "location": "Building A, Floor 2", "head": "Dr. Smith"},
            {"id": 2, "name": "Neurology", "description": "Brain and nervous system",
             "location": "Building B, Floor 1", "head": "Dr. Johnson"},
            {"id": 3, "name": "Pediatrics", "description": "Medical care for infants, children, and adolescents",
             "location": "Building C, Floor 3", "head": "Dr. Williams"},
            {"id": 4, "name": "Orthopedics", "description": "Musculoskeletal system",
             "location": "Building A, Floor 3", "head": "Dr. Brown"},
            {"id": 5, "name": "Oncology", "description": "Cancer treatment",
             "location": "Building D, Floor 2", "head": "Dr. Davis"}
        ]

        # Add departments to the model
        for dept in sample_departments:
            row_items = [
                QStandardItem(str(dept["id"])),
                QStandardItem(dept["name"]),
                QStandardItem(dept["description"]),
                QStandardItem(dept["location"]),
                QStandardItem(dept["head"])
            ]
            self.departments_model.appendRow(row_items)

        # Resize columns to content
        self.departments_table.resizeColumnsToContents()

    def add_department(self):
        """Open dialog to add a new department"""
        dialog = DepartmentForm(self)
        if dialog.exec():
            department_data = dialog.get_department_data()

            # Validate input
            if not department_data["name"]:
                QMessageBox.warning(self, "Error", "Department name is required.")
                return

            # Generate new ID (in a real app, this would be done by the database)
            new_id = self.departments_model.rowCount() + 1

            # Add to model
            row_items = [
                QStandardItem(str(new_id)),
                QStandardItem(department_data["name"]),
                QStandardItem(department_data["description"]),
                QStandardItem(department_data["location"]),
                QStandardItem(department_data["head"])
            ]
            self.departments_model.appendRow(row_items)

            QMessageBox.information(self, "Success", f"Department '{department_data['name']}' added successfully.")

    def edit_department(self):
        """Open dialog to edit the selected department"""
        selected_indexes = self.departments_table.selectedIndexes()
        if not selected_indexes:
            QMessageBox.warning(self, "Error", "Please select a department to edit.")
            return

        # Get the row of the first selected cell
        row = selected_indexes[0].row()

        # Get department data from the model
        department_data = {
            "id": self.departments_model.item(row, 0).text(),
            "name": self.departments_model.item(row, 1).text(),
            "description": self.departments_model.item(row, 2).text(),
            "location": self.departments_model.item(row, 3).text(),
            "head": self.departments_model.item(row, 4).text()
        }

        # Open dialog with department data
        dialog = DepartmentForm(self, department_data)
        if dialog.exec():
            updated_data = dialog.get_department_data()

            # Validate input
            if not updated_data["name"]:
                QMessageBox.warning(self, "Error", "Department name is required.")
                return

            # Update model
            self.departments_model.item(row, 1).setText(updated_data["name"])
            self.departments_model.item(row, 2).setText(updated_data["description"])
            self.departments_model.item(row, 3).setText(updated_data["location"])
            self.departments_model.item(row, 4).setText(updated_data["head"])

            QMessageBox.information(self, "Success", f"Department '{updated_data['name']}' updated successfully.")

    def delete_department(self):
        """Delete the selected department"""
        selected_indexes = self.departments_table.selectedIndexes()
        if not selected_indexes:
            QMessageBox.warning(self, "Error", "Please select a department to delete.")
            return

        # Get the row of the first selected cell
        row = selected_indexes[0].row()

        # Get department name
        department_name = self.departments_model.item(row, 1).text()

        # Confirm deletion
        reply = QMessageBox.question(self, "Confirm Deletion",
                                    f"Are you sure you want to delete department '{department_name}'?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # Remove from model
            self.departments_model.removeRow(row)

            QMessageBox.information(self, "Success", f"Department '{department_name}' deleted successfully.")
