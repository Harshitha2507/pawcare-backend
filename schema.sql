-- schema.sql
CREATE DATABASE IF NOT EXISTS pawcare_db;
USE pawcare_db;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'adopter', -- 'adopter' or 'lender'
    lender_type VARCHAR(50), -- NGO, Rescuer, Pet Owner
    location VARCHAR(100)
);

-- Pets Table (Updated to match Frontend)
CREATE TABLE IF NOT EXISTS pets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50), -- Dogs, Cats, etc.
    breed VARCHAR(100),
    image VARCHAR(500), -- URL to image
    location VARCHAR(100),
    age VARCHAR(50),
    sex VARCHAR(20),
    color VARCHAR(50),
    description TEXT,
    health_status VARCHAR(100),
    album TEXT,
    is_favorited BOOLEAN DEFAULT FALSE,
    status VARCHAR(20) DEFAULT 'available', -- 'available' or 'adopted'
    lender_id INT, -- Link to user who posted it
    FOREIGN KEY (lender_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Applications Table
CREATE TABLE IF NOT EXISTS applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pet_id INT,
    adopter_id INT, -- Link to user who is applying
    applicant_name VARCHAR(100),
    applicant_email VARCHAR(100),
    phone VARCHAR(20),
    address TEXT,
    message TEXT,
    status VARCHAR(20) DEFAULT 'Pending', -- Pending, Approved, Rejected
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pet_id) REFERENCES pets(id) ON DELETE CASCADE,
    FOREIGN KEY (adopter_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Chats Table
CREATE TABLE IF NOT EXISTS chats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user1_id INT, -- Adopter
    user2_id INT, -- Lender
    pet_id INT,   -- Associated pet (optional context)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user1_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (user2_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (pet_id) REFERENCES pets(id) ON DELETE SET NULL
);

-- Messages Table
CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    chat_id INT,
    sender_id INT,
    receiver_id INT,
    message TEXT,
    is_read BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chat_id) REFERENCES chats(id) ON DELETE CASCADE,
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Notifications Table
CREATE TABLE IF NOT EXISTS notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT, -- Recipient
    application_id INT, -- Link to specific application (optional)
    title VARCHAR(255),
    message TEXT,
    type VARCHAR(50) DEFAULT 'general', -- 'mid_priority' (health/new_pet) or 'high_priority' (app_update)
    scheduled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Visible only after this time
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE CASCADE
);
