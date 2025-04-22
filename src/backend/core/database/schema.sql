-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'finance', 'doctor', 'department_head', 'administration')),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    mfa_enabled BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Departments table
CREATE TABLE IF NOT EXISTS departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    head_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Doctors table
CREATE TABLE IF NOT EXISTS doctors (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    department_id INTEGER REFERENCES departments(id) ON DELETE SET NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    specialization VARCHAR(100),
    license_number VARCHAR(50) UNIQUE,
    mobile VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Patients table
CREATE TABLE IF NOT EXISTS patients (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    dob DATE NOT NULL,
    gender VARCHAR(10) CHECK (gender IN ('male', 'female', 'other')),
    address TEXT,
    mobile VARCHAR(15),
    email VARCHAR(100),
    emergency_contact_name VARCHAR(100),
    emergency_contact_mobile VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Visits table
CREATE TABLE IF NOT EXISTS visits (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(id) ON DELETE CASCADE,
    doctor_id INTEGER REFERENCES doctors(id) ON DELETE SET NULL,
    visit_date TIMESTAMP NOT NULL,
    reason TEXT,
    diagnosis TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Consultations table
CREATE TABLE IF NOT EXISTS consultations (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(id) ON DELETE CASCADE,
    doctor_id INTEGER REFERENCES doctors(id) ON DELETE SET NULL,
    department_id INTEGER REFERENCES departments(id) ON DELETE SET NULL,
    scheduled_date TIMESTAMP NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('pending', 'confirmed', 'completed', 'cancelled')),
    consultation_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Diagnostics table
CREATE TABLE IF NOT EXISTS diagnostics (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(id) ON DELETE CASCADE,
    visit_id INTEGER REFERENCES visits(id) ON DELETE SET NULL,
    doctor_id INTEGER REFERENCES doctors(id) ON DELETE SET NULL,
    test_name VARCHAR(100) NOT NULL,
    test_date TIMESTAMP NOT NULL,
    result TEXT,
    reference_range TEXT,
    unit VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Prescriptions table
CREATE TABLE IF NOT EXISTS prescriptions (
    id SERIAL PRIMARY KEY,
    visit_id INTEGER REFERENCES visits(id) ON DELETE CASCADE,
    patient_id INTEGER REFERENCES patients(id) ON DELETE CASCADE,
    doctor_id INTEGER REFERENCES doctors(id) ON DELETE SET NULL,
    medicine_name VARCHAR(100) NOT NULL,
    dosage VARCHAR(50),
    frequency VARCHAR(50),
    duration VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Medical Analytics table
CREATE TABLE IF NOT EXISTS medical_analytics (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(id) ON DELETE CASCADE,
    diagnostic_id INTEGER REFERENCES diagnostics(id) ON DELETE SET NULL,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(10,2),
    metric_date TIMESTAMP NOT NULL,
    trend VARCHAR(20) CHECK (trend IN ('improving', 'stable', 'worsening', 'unknown')),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Doctor KPI table
CREATE TABLE IF NOT EXISTS doctor_kpi (
    id SERIAL PRIMARY KEY,
    doctor_id INTEGER REFERENCES doctors(id) ON DELETE CASCADE,
    department_id INTEGER REFERENCES departments(id) ON DELETE SET NULL,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(10,2),
    metric_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Department KPI table
CREATE TABLE IF NOT EXISTS department_kpi (
    id SERIAL PRIMARY KEY,
    department_id INTEGER REFERENCES departments(id) ON DELETE CASCADE,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(10,2),
    metric_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Transactions table
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(id) ON DELETE SET NULL,
    visit_id INTEGER REFERENCES visits(id) ON DELETE SET NULL,
    consultation_id INTEGER REFERENCES consultations(id) ON DELETE SET NULL,
    amount DECIMAL(10,2) NOT NULL,
    transaction_type VARCHAR(50) NOT NULL CHECK (transaction_type IN ('payment', 'refund', 'expense')),
    description TEXT,
    payment_method VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Central Hospital Account table
CREATE TABLE IF NOT EXISTS hospital_account (
    id SERIAL PRIMARY KEY,
    transaction_id INTEGER UNIQUE REFERENCES transactions(id) ON DELETE CASCADE,
    balance DECIMAL(10,2) NOT NULL,
    transaction_date TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Doctor Expenses table
CREATE TABLE IF NOT EXISTS doctor_expenses (
    id SERIAL PRIMARY KEY,
    doctor_id INTEGER REFERENCES doctors(id) ON DELETE CASCADE,
    expense_type VARCHAR(50) NOT NULL CHECK (expense_type IN ('salary', 'bonus', 'equipment', 'other')),
    amount DECIMAL(10,2) NOT NULL,
    description TEXT,
    expense_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Audit Log table
CREATE TABLE IF NOT EXISTS audit_log (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id INTEGER NOT NULL,
    details JSONB,
    ip_address VARCHAR(45),
    session_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for audit log performance
CREATE INDEX idx_audit_log_user_id ON audit_log(user_id);
CREATE INDEX idx_audit_log_entity_type ON audit_log(entity_type);
CREATE INDEX idx_audit_log_entity_id ON audit_log(entity_id);
CREATE INDEX idx_audit_log_created_at ON audit_log(created_at);

-- Function to log audit actions
CREATE OR REPLACE FUNCTION log_audit_action(
    p_user_id INTEGER,
    p_action VARCHAR,
    p_entity_type VARCHAR,
    p_entity_id INTEGER,
    p_details JSONB,
    p_ip_address VARCHAR,
    p_session_id VARCHAR
) RETURNS VOID AS $$
BEGIN
    INSERT INTO audit_log (
        user_id, action, entity_type, entity_id, details, ip_address, session_id, created_at
    ) VALUES (
        p_user_id, p_action, p_entity_type, p_entity_id, p_details, p_ip_address, p_session_id, CURRENT_TIMESTAMP
    );
END;
$$ LANGUAGE plpgsql;

-- Generic audit trigger function
CREATE OR REPLACE FUNCTION audit_trigger_function() RETURNS TRIGGER AS $$
DECLARE
    details JSONB;
    user_id INTEGER;
    ip_address VARCHAR;
    session_id VARCHAR;
BEGIN
    user_id := NULLIF(current_setting('medisys.user_id', TRUE), '')::INTEGER;
    ip_address := current_setting('medisys.ip_address', TRUE);
    session_id := current_setting('medisys.session_id', TRUE);

    IF TG_OP = 'INSERT' THEN
        details := jsonb_build_object('new', to_jsonb(NEW));
        PERFORM log_audit_action(
            user_id, 'create_' || TG_TABLE_NAME, TG_TABLE_NAME, NEW.id, details, ip_address, session_id
        );
    ELSIF TG_OP = 'UPDATE' THEN
        details := jsonb_build_object('old', to_jsonb(OLD), 'new', to_jsonb(NEW));
        PERFORM log_audit_action(
            user_id, 'update_' || TG_TABLE_NAME, TG_TABLE_NAME, NEW.id, details, ip_address, session_id
        );
    ELSIF TG_OP = 'DELETE' THEN
        details := jsonb_build_object('old', to_jsonb(OLD));
        PERFORM log_audit_action(
            user_id, 'delete_' || TG_TABLE_NAME, TG_TABLE_NAME, OLD.id, details, ip_address, session_id
        );
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Apply audit triggers
DO $$
BEGIN
    FOR table_name IN (
        'users', 'departments', 'doctors', 'patients', 'visits', 
        'consultations', 'diagnostics', 'prescriptions', 'medical_analytics',
        'doctor_kpi', 'department_kpi', 'transactions', 'hospital_account', 'doctor_expenses'
    ) LOOP
        EXECUTE format('
            CREATE TRIGGER audit_%s_trigger
            AFTER INSERT OR UPDATE OR DELETE ON %s
            FOR EACH ROW
            EXECUTE FUNCTION audit_trigger_function();
        ', table_name, table_name);
    END LOOP;
END $$;

-- Update timestamp trigger function
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply update timestamp triggers
DO $$
BEGIN
    FOR table_name IN (
        'users', 'departments', 'doctors', 'patients', 'visits', 
        'consultations', 'diagnostics', 'prescriptions', 'medical_analytics',
        'doctor_kpi', 'department_kpi', 'transactions', 'hospital_account', 'doctor_expenses'
    ) LOOP
        EXECUTE format('
            CREATE TRIGGER update_%s_timestamp
            BEFORE UPDATE ON %s
            FOR EACH ROW
            EXECUTE FUNCTION update_timestamp();
        ', table_name, table_name);
    END LOOP;
END $$;

-- Role-based access
CREATE ROLE admin_role;
CREATE ROLE doctor_role;
CREATE ROLE finance_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO admin_role;
GRANT SELECT, INSERT, UPDATE ON visits, prescriptions, diagnostics TO doctor_role;
GRANT SELECT, INSERT, UPDATE ON transactions, hospital_account TO finance_role;
GRANT SELECT ON audit_log TO admin_role;
REVOKE ALL ON audit_log FROM doctor_role, finance_role;

-- Row-level security
ALTER TABLE patients ENABLE ROW LEVEL SECURITY;
CREATE POLICY doctor_access ON patients
    FOR ALL
    TO doctor_role
    USING (id IN (
        SELECT patient_id FROM visits WHERE doctor_id = (SELECT id FROM doctors WHERE user_id = current_user::INTEGER)
    ));

-- Audit summary view
CREATE VIEW audit_summary AS
SELECT 
    u.username,
    al.action,
    al.entity_type,
    al.entity_id,
    al.details,
    al.ip_address,
    al.session_id,
    al.created_at
FROM audit_log al
LEFT JOIN users u ON al.user_id = u.id
ORDER BY al.created_at DESC;