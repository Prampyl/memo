-- Enable UUID extension for secure, unique identifiers
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. HUMAN ENTITIES

CREATE TABLE IF NOT EXISTS Address (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    street_line_1 VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    zip_code VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS Patient (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    address_id UUID REFERENCES Address(id) ON DELETE SET NULL,
    first_name VARCHAR(100) NOT NULL, last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL, diagnosis_stage VARCHAR(50), 
    preferred_name VARCHAR(100), profile_picture_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Caregiver (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    address_id UUID REFERENCES Address(id) ON DELETE SET NULL,
    patient_id UUID NOT NULL REFERENCES Patient(id) ON DELETE CASCADE,
    email VARCHAR(255) UNIQUE NOT NULL, password_hash VARCHAR(255) NOT NULL, 
    first_name VARCHAR(100) NOT NULL, 
    last_name VARCHAR(100) NOT NULL,
    relationship VARCHAR(100), -- Ex: 'Daughter', 'Son', 'Nurse'
    phone_number VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Doctor (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    full_name VARCHAR(200) NOT NULL, specialty VARCHAR(100), 
    phone_number VARCHAR(50) UNIQUE NOT NULL, 
    email VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS PatientDoctor (
    patient_id UUID REFERENCES Patient(id) ON DELETE CASCADE,
    doctor_id UUID REFERENCES Doctor(id) ON DELETE CASCADE,
    PRIMARY KEY (patient_id, doctor_id)
);

-- 2. SCHEDULING & HARDWARE
CREATE TABLE IF NOT EXISTS Reminder (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID REFERENCES Patient(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL, spoken_message TEXT NOT NULL, 
    scheduled_time TIME NOT NULL, category VARCHAR(50) NOT NULL, is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS Device (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    serial_number VARCHAR(100) UNIQUE NOT NULL,
    patient_id UUID REFERENCES Patient(id), 
    status VARCHAR(50) DEFAULT 'Offline', settings JSONB, last_seen_at TIMESTAMP WITH TIME ZONE
);

-- 3. AI CONTENT
CREATE TABLE IF NOT EXISTS VoiceProfile (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID REFERENCES Patient(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL, provider_voice_id VARCHAR(255) NOT NULL, is_active BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS MediaItem (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID REFERENCES Patient(id) ON DELETE CASCADE, -- Fixed: was 'Patient'
    file_path TEXT NOT NULL, media_type VARCHAR(20) NOT NULL, 
    description TEXT, is_favorite BOOLEAN DEFAULT FALSE
);

-- 4. COGNITIVE TRACKING
CREATE TABLE IF NOT EXISTS CognitiveExercise (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(200) NOT NULL, type VARCHAR(50) NOT NULL, 
    difficulty_level INTEGER CHECK (difficulty_level BETWEEN 1 AND 5)
);

CREATE TABLE IF NOT EXISTS ExerciseLog (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID REFERENCES Patient(id) ON DELETE CASCADE,
    exercise_id UUID REFERENCES CognitiveExercise(id), -- Fixed: was 'CognitiveExercise'
    score INTEGER, played_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);