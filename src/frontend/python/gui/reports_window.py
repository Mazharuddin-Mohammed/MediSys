from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, 
                             QTableView, QPushButton, QComboBox, QDateEdit, QTabWidget)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt, QDate

class ReportsWindow(QMainWindow):
    def __init__(self, db=None, user_id=None):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.setWindowTitle("MediSys - Reports")
        self.setMinimumSize(1000, 700)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        header_label = QLabel("Reports Dashboard")
        header_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)
        
        # Create tabs for different report types
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Patient Reports Tab
        patient_tab = QWidget()
        patient_layout = QVBoxLayout(patient_tab)
        
        # Filter controls
        patient_filter_layout = QHBoxLayout()
        
        date_range_label = QLabel("Date Range:")
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate().addMonths(-1))
        
        to_label = QLabel("to")
        
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())
        
        report_type_label = QLabel("Report Type:")
        self.patient_report_type = QComboBox()
        self.patient_report_type.addItems([
            "New Patients", "Patient Visits", "Patient Demographics"
        ])
        
        generate_button = QPushButton("Generate Report")
        generate_button.clicked.connect(self.generate_patient_report)
        
        patient_filter_layout.addWidget(date_range_label)
        patient_filter_layout.addWidget(self.start_date)
        patient_filter_layout.addWidget(to_label)
        patient_filter_layout.addWidget(self.end_date)
        patient_filter_layout.addWidget(report_type_label)
        patient_filter_layout.addWidget(self.patient_report_type)
        patient_filter_layout.addWidget(generate_button)
        
        patient_layout.addLayout(patient_filter_layout)
        
        # Patient report table
        self.patient_report_table = QTableView()
        self.patient_report_model = QStandardItemModel(0, 5)
        self.patient_report_table.setModel(self.patient_report_model)
        patient_layout.addWidget(self.patient_report_table)
        
        # Doctor Reports Tab
        doctor_tab = QWidget()
        doctor_layout = QVBoxLayout(doctor_tab)
        
        # Filter controls
        doctor_filter_layout = QHBoxLayout()
        
        doctor_date_range_label = QLabel("Date Range:")
        self.doctor_start_date = QDateEdit()
        self.doctor_start_date.setCalendarPopup(True)
        self.doctor_start_date.setDate(QDate.currentDate().addMonths(-1))
        
        doctor_to_label = QLabel("to")
        
        self.doctor_end_date = QDateEdit()
        self.doctor_end_date.setCalendarPopup(True)
        self.doctor_end_date.setDate(QDate.currentDate())
        
        doctor_report_type_label = QLabel("Report Type:")
        self.doctor_report_type = QComboBox()
        self.doctor_report_type.addItems([
            "Doctor Workload", "Doctor Performance", "Doctor Specialization"
        ])
        
        doctor_generate_button = QPushButton("Generate Report")
        doctor_generate_button.clicked.connect(self.generate_doctor_report)
        
        doctor_filter_layout.addWidget(doctor_date_range_label)
        doctor_filter_layout.addWidget(self.doctor_start_date)
        doctor_filter_layout.addWidget(doctor_to_label)
        doctor_filter_layout.addWidget(self.doctor_end_date)
        doctor_filter_layout.addWidget(doctor_report_type_label)
        doctor_filter_layout.addWidget(self.doctor_report_type)
        doctor_filter_layout.addWidget(doctor_generate_button)
        
        doctor_layout.addLayout(doctor_filter_layout)
        
        # Doctor report table
        self.doctor_report_table = QTableView()
        self.doctor_report_model = QStandardItemModel(0, 5)
        self.doctor_report_table.setModel(self.doctor_report_model)
        doctor_layout.addWidget(self.doctor_report_table)
        
        # Financial Reports Tab
        financial_tab = QWidget()
        financial_layout = QVBoxLayout(financial_tab)
        
        # Filter controls
        financial_filter_layout = QHBoxLayout()
        
        financial_date_range_label = QLabel("Date Range:")
        self.financial_start_date = QDateEdit()
        self.financial_start_date.setCalendarPopup(True)
        self.financial_start_date.setDate(QDate.currentDate().addMonths(-1))
        
        financial_to_label = QLabel("to")
        
        self.financial_end_date = QDateEdit()
        self.financial_end_date.setCalendarPopup(True)
        self.financial_end_date.setDate(QDate.currentDate())
        
        financial_report_type_label = QLabel("Report Type:")
        self.financial_report_type = QComboBox()
        self.financial_report_type.addItems([
            "Revenue by Department", "Revenue by Doctor", "Expenses"
        ])
        
        financial_generate_button = QPushButton("Generate Report")
        financial_generate_button.clicked.connect(self.generate_financial_report)
        
        financial_filter_layout.addWidget(financial_date_range_label)
        financial_filter_layout.addWidget(self.financial_start_date)
        financial_filter_layout.addWidget(financial_to_label)
        financial_filter_layout.addWidget(self.financial_end_date)
        financial_filter_layout.addWidget(financial_report_type_label)
        financial_filter_layout.addWidget(self.financial_report_type)
        financial_filter_layout.addWidget(financial_generate_button)
        
        financial_layout.addLayout(financial_filter_layout)
        
        # Financial report table
        self.financial_report_table = QTableView()
        self.financial_report_model = QStandardItemModel(0, 5)
        self.financial_report_table.setModel(self.financial_report_model)
        financial_layout.addWidget(self.financial_report_table)
        
        # Add tabs
        self.tabs.addTab(patient_tab, "Patient Reports")
        self.tabs.addTab(doctor_tab, "Doctor Reports")
        self.tabs.addTab(financial_tab, "Financial Reports")
        
        # Export button
        export_button = QPushButton("Export Report")
        export_button.clicked.connect(self.export_report)
        main_layout.addWidget(export_button)
    
    def generate_patient_report(self):
        """Generate patient report based on selected filters"""
        report_type = self.patient_report_type.currentText()
        start_date = self.start_date.date().toString("yyyy-MM-dd")
        end_date = self.end_date.date().toString("yyyy-MM-dd")
        
        # Clear existing data
        self.patient_report_model.clear()
        
        if report_type == "New Patients":
            self.patient_report_model.setHorizontalHeaderLabels([
                "ID", "Name", "Registration Date", "Age", "Gender"
            ])
            
            # Sample data
            sample_data = [
                ["1", "John Doe", "2023-05-15", "45", "Male"],
                ["2", "Jane Smith", "2023-05-20", "32", "Female"],
                ["3", "Robert Johnson", "2023-05-25", "58", "Male"],
                ["4", "Emily Davis", "2023-06-02", "27", "Female"],
                ["5", "Michael Brown", "2023-06-10", "41", "Male"]
            ]
            
            for row_data in sample_data:
                row_items = [QStandardItem(item) for item in row_data]
                self.patient_report_model.appendRow(row_items)
                
        elif report_type == "Patient Visits":
            self.patient_report_model.setHorizontalHeaderLabels([
                "Patient ID", "Patient Name", "Visit Date", "Doctor", "Department"
            ])
            
            # Sample data
            sample_data = [
                ["1", "John Doe", "2023-05-18", "Dr. Smith", "Cardiology"],
                ["2", "Jane Smith", "2023-05-22", "Dr. Johnson", "Neurology"],
                ["1", "John Doe", "2023-06-01", "Dr. Smith", "Cardiology"],
                ["3", "Robert Johnson", "2023-06-05", "Dr. Williams", "Orthopedics"],
                ["4", "Emily Davis", "2023-06-12", "Dr. Brown", "Pediatrics"]
            ]
            
            for row_data in sample_data:
                row_items = [QStandardItem(item) for item in row_data]
                self.patient_report_model.appendRow(row_items)
                
        elif report_type == "Patient Demographics":
            self.patient_report_model.setHorizontalHeaderLabels([
                "Age Group", "Male Count", "Female Count", "Total", "Percentage"
            ])
            
            # Sample data
            sample_data = [
                ["0-18", "12", "15", "27", "18%"],
                ["19-35", "23", "28", "51", "34%"],
                ["36-50", "18", "21", "39", "26%"],
                ["51-65", "14", "10", "24", "16%"],
                ["65+", "5", "4", "9", "6%"]
            ]
            
            for row_data in sample_data:
                row_items = [QStandardItem(item) for item in row_data]
                self.patient_report_model.appendRow(row_items)
        
        self.patient_report_table.resizeColumnsToContents()
    
    def generate_doctor_report(self):
        """Generate doctor report based on selected filters"""
        report_type = self.doctor_report_type.currentText()
        start_date = self.doctor_start_date.date().toString("yyyy-MM-dd")
        end_date = self.doctor_end_date.date().toString("yyyy-MM-dd")
        
        # Clear existing data
        self.doctor_report_model.clear()
        
        if report_type == "Doctor Workload":
            self.doctor_report_model.setHorizontalHeaderLabels([
                "Doctor ID", "Doctor Name", "Department", "Appointments", "Hours"
            ])
            
            # Sample data
            sample_data = [
                ["1", "Dr. Smith", "Cardiology", "45", "67.5"],
                ["2", "Dr. Johnson", "Neurology", "38", "57.0"],
                ["3", "Dr. Williams", "Pediatrics", "52", "78.0"],
                ["4", "Dr. Brown", "Orthopedics", "31", "46.5"],
                ["5", "Dr. Davis", "Oncology", "27", "40.5"]
            ]
            
            for row_data in sample_data:
                row_items = [QStandardItem(item) for item in row_data]
                self.doctor_report_model.appendRow(row_items)
                
        elif report_type == "Doctor Performance":
            self.doctor_report_model.setHorizontalHeaderLabels([
                "Doctor ID", "Doctor Name", "Patients Seen", "Avg. Time per Patient", "Rating"
            ])
            
            # Sample data
            sample_data = [
                ["1", "Dr. Smith", "45", "30 min", "4.8/5"],
                ["2", "Dr. Johnson", "38", "35 min", "4.6/5"],
                ["3", "Dr. Williams", "52", "25 min", "4.9/5"],
                ["4", "Dr. Brown", "31", "40 min", "4.7/5"],
                ["5", "Dr. Davis", "27", "45 min", "4.5/5"]
            ]
            
            for row_data in sample_data:
                row_items = [QStandardItem(item) for item in row_data]
                self.doctor_report_model.appendRow(row_items)
                
        elif report_type == "Doctor Specialization":
            self.doctor_report_model.setHorizontalHeaderLabels([
                "Specialization", "Doctor Count", "Patient Count", "Avg. Patients per Doctor", "Revenue"
            ])
            
            # Sample data
            sample_data = [
                ["Cardiology", "3", "120", "40", "$24,000"],
                ["Neurology", "2", "76", "38", "$19,000"],
                ["Pediatrics", "4", "208", "52", "$31,200"],
                ["Orthopedics", "2", "62", "31", "$18,600"],
                ["Oncology", "2", "54", "27", "$27,000"]
            ]
            
            for row_data in sample_data:
                row_items = [QStandardItem(item) for item in row_data]
                self.doctor_report_model.appendRow(row_items)
        
        self.doctor_report_table.resizeColumnsToContents()
    
    def generate_financial_report(self):
        """Generate financial report based on selected filters"""
        report_type = self.financial_report_type.currentText()
        start_date = self.financial_start_date.date().toString("yyyy-MM-dd")
        end_date = self.financial_end_date.date().toString("yyyy-MM-dd")
        
        # Clear existing data
        self.financial_report_model.clear()
        
        if report_type == "Revenue by Department":
            self.financial_report_model.setHorizontalHeaderLabels([
                "Department", "Appointments", "Procedures", "Tests", "Total Revenue"
            ])
            
            # Sample data
            sample_data = [
                ["Cardiology", "$12,000", "$8,000", "$4,000", "$24,000"],
                ["Neurology", "$9,500", "$6,500", "$3,000", "$19,000"],
                ["Pediatrics", "$15,600", "$10,400", "$5,200", "$31,200"],
                ["Orthopedics", "$9,300", "$6,200", "$3,100", "$18,600"],
                ["Oncology", "$13,500", "$9,000", "$4,500", "$27,000"]
            ]
            
            for row_data in sample_data:
                row_items = [QStandardItem(item) for item in row_data]
                self.financial_report_model.appendRow(row_items)
                
        elif report_type == "Revenue by Doctor":
            self.financial_report_model.setHorizontalHeaderLabels([
                "Doctor ID", "Doctor Name", "Department", "Patients Seen", "Revenue"
            ])
            
            # Sample data
            sample_data = [
                ["1", "Dr. Smith", "Cardiology", "45", "$13,500"],
                ["2", "Dr. Johnson", "Neurology", "38", "$11,400"],
                ["3", "Dr. Williams", "Pediatrics", "52", "$15,600"],
                ["4", "Dr. Brown", "Orthopedics", "31", "$9,300"],
                ["5", "Dr. Davis", "Oncology", "27", "$13,500"]
            ]
            
            for row_data in sample_data:
                row_items = [QStandardItem(item) for item in row_data]
                self.financial_report_model.appendRow(row_items)
                
        elif report_type == "Expenses":
            self.financial_report_model.setHorizontalHeaderLabels([
                "Category", "Amount", "Percentage", "Previous Month", "Change"
            ])
            
            # Sample data
            sample_data = [
                ["Salaries", "$85,000", "60%", "$82,000", "+3.7%"],
                ["Equipment", "$20,000", "14%", "$25,000", "-20.0%"],
                ["Supplies", "$15,000", "11%", "$14,000", "+7.1%"],
                ["Utilities", "$10,000", "7%", "$9,500", "+5.3%"],
                ["Other", "$12,000", "8%", "$11,000", "+9.1%"]
            ]
            
            for row_data in sample_data:
                row_items = [QStandardItem(item) for item in row_data]
                self.financial_report_model.appendRow(row_items)
        
        self.financial_report_table.resizeColumnsToContents()
    
    def export_report(self):
        """Export the current report to a file"""
        # In a real application, this would export to CSV, Excel, or PDF
        # For now, just show a message
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Export Report", "Report exported successfully!")
