-- TODO: Define Patients Table
CREATE TABLE patients (
  id UUID PRIMARY KEY,
  name TEXT NOT NULL,
  diagnosis TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- TODO: Define Reminders Table
CREATE TABLE reminders (
  id UUID PRIMARY KEY,
  patient_id UUID REFERENCES patients(id),
  schedule_time TIMESTAMP NOT NULL,
  status VARCHAR(20) DEFAULT 'PENDING'
);
