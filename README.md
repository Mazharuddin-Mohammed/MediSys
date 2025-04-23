# MediSys

MediSys is a comprehensive hospital management system with a modular architecture, featuring a C++ backend, PostgreSQL database, and PySide6 GUI with Vulkan rendering. The application provides dedicated modules for different aspects of hospital management, each opening in separate windows with their own specialized features.

![MediSys Banner](src/frontend/python/resources/images/medisys_banner.png)

## Features

### Admin Dashboard
- System overview with key metrics
- User management and access control
- Comprehensive audit logging for security and compliance
- Quick access to all modules

### Patients Module
- Complete patient record management
- Add, edit, and delete patient information
- View patient medical history
- Search functionality for quick access to patient records

### Departments Module
- Department creation and management
- Track department resources and staff
- Department-specific settings and configurations

### Doctors Module
- Doctor profile management
- Specialization and department assignment
- Track doctor workload and performance

### Appointments Module
- Calendar-based appointment scheduling
- Filter appointments by date, doctor, or status
- Appointment creation, modification, and cancellation

### Reports Module
- Generate various types of reports (patient, doctor, financial)
- Date range filtering for reports
- Export functionality for data analysis

## Technical Architecture

### Backend (C++)
- Core business logic implemented in C++
- PostgreSQL database integration using libpqxx
- Python bindings via pybind11
- Modular design with service-oriented architecture

### Frontend (Python/PySide6)
- Modern GUI built with PySide6 (Qt for Python)
- Dedicated window for each module
- Responsive design with proper layouts
- Vulkan rendering for hardware acceleration

### Database
- PostgreSQL for robust data storage
- Proper schema with relationships between entities
- Transaction support for data integrity
- Audit logging for all critical operations

## Setup

### Prerequisites
- PostgreSQL 13+
- Python 3.10+
- CMake 3.15+
- C++17 compatible compiler
- Vulkan SDK 1.2+
- Qt dependencies for PySide6

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/medisys.git
   cd medisys
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python requirements:
   ```bash
   pip install -r requirements.txt
   ```

4. Setup the database:
   ```bash
   ./scripts/setup_db.sh
   ```

5. Build the C++ backend:
   ```bash
   ./scripts/build.sh
   ```

6. Run the application:
   ```bash
   python run_app.py
   ```

## Default Login
- Username: admin
- Password: admin

## Contributing
Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.

## Author
Mazharuddin Mohammed