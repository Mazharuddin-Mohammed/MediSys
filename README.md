# MediSys

MediSys is a modular, scalable desktop application for hospital management, supporting multiple user roles (Admin, Finance, Departments, Doctors, Patients) with a C++ backend, PostgreSQL database, and PySide6 GUI with Vulkan rendering.

![MediSys Banner](src/frontend/python/resources/images/medisys_banner.png)

## Features
- Role-based access for Admin, Finance, Doctors, and more.
- Patient management with visit history, diagnostics, and prescriptions.
- Financial tracking with billing and invoicing.
- KPI analytics for doctors and departments.
- Comprehensive audit logging for security and compliance.

## Setup
1. Install dependencies:
   - PostgreSQL
   - Python 3.10+
   - CMake
   - Vulkan SDK

2. Install Python requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Build the C++ backend:
   ```bash
   mkdir build
   cd build
   cmake ..
   make
   ```
4. Run the application:
   ```bash
   python main.py
   ```
5. Setup database:
   ./scripts/setup_db.sh

6. Build and run:
   ./scripts/build.sh
   ./scripts/run.sh


## Contributing
Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.