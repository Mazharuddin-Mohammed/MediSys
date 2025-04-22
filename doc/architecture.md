# MediSys Architecture

MediSys is a hospital management system with a C++ backend, PostgreSQL database, and PySide6 GUI using Vulkan rendering.

## Components
- **Backend**: C++ with PostgreSQL (libpqxx) for data management.
  - **Database**: Schema with users, patients, doctors, visits, transactions, and audit logs.
  - **Services**: AuthService, PatientService, etc., for business logic.
  - **Bindings**: Pybind11 for Python integration.
- **Frontend**: PySide6 GUI with Vulkan for high-performance rendering.
  - **GUI**: LoginWindow, AdminWindow, DoctorWindow, PatientWindow.
  - **Analytics**: KPI and medical analytics using pandas/matplotlib.
  - **Billing**: Invoice generation with MediSys branding.
- **Resources**: Logo (`medisys_logo.png`), banner (`medisys_banner.png`), and QSS styles.
- **Security**: SSL/TLS, pgcrypto, RLS, bcrypt, audit logging.
- **Audit Logging**: Tracks all actions with user_id, ip_address, session_id, and JSONB details.

## Branding
- **Name**: MediSys
- **Logo**: Caduceus with digital waveform in blue/green.
- **Banner**: Gradient background with logo and tagline.
- **Usage**: Logo in GUI icons, banner in GUI headers and invoices.