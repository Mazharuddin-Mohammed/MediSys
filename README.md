# MediSys

MediSys is a comprehensive hospital management system with a modular architecture, featuring a C++ backend, PostgreSQL database, and PySide6 GUI with Vulkan rendering. The application provides dedicated modules for different aspects of hospital management, each opening in separate windows with their own specialized features.

![MediSys Banner](src/frontend/python/resources/images/medisys_banner.png)

## Screenshots

### Login Screen
![Login Screen](src/frontend/python/resources/images/screenshots/login_screen.png)

### Admin Dashboard
![Admin Dashboard](src/frontend/python/resources/images/screenshots/admin_dashboard.png)

### Patient Management
![Patient Management](src/frontend/python/resources/images/screenshots/patient_management.png)

### Doctor Dashboard
![Doctor Dashboard](src/frontend/python/resources/images/screenshots/doctor_dashboard.png)

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
- Patient photo management with placeholder images

### Departments Module
- Department creation and management
- Track department resources and staff
- Department-specific settings and configurations

### Doctors Module
- Doctor profile management
- Specialization and department assignment
- Track doctor workload and performance
- Doctor photo management with placeholder images

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

## Default Login Credentials

### Admin User
- Username: admin
- Password: admin

### Doctor User
- Username: doctor
- Password: doctor123

## Contributing
Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.

## Support the Project

[![Buy Me A Coffee](src/frontend/python/resources/images/buy_me_coffee.svg)](https://buymeacoffee.com/mazharm)

Hi, I'm a passionate scientist dedicated to bridging the gap between academia and industry through research exploitation and knowledge transfer. My work focuses on turning cutting-edge academic discoveries into practical, real-world solutions that drive innovation and impact. By fostering collaboration and translating complex research into accessible applications, I aim to create a seamless flow of knowledge that benefits both worlds.

If you'd like to support my mission to connect ideas with impact, consider buying me a coffee! Your support helps fuel my efforts to build stronger bridges between researchers and industry innovators. Thank you for being part of this journey!

## Author
Mazharuddin Mohammed