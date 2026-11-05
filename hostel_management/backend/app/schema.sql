-- Run this file ONCE to create the database and all tables.
-- Command:  mysql -u root -p < schema.sql

CREATE DATABASE IF NOT EXISTS hostel_db;
USE hostel_db;

-- Login accounts (admins and students both log in through this table)
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'student') NOT NULL DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,               -- links to the login account
    student_name VARCHAR(100) NOT NULL,
    email VARCHAR(150),
    phone VARCHAR(20),
    course VARCHAR(100),
    year VARCHAR(20),                          -- text like "2nd Year", so VARCHAR not INT
    parent_name VARCHAR(100),
    parent_phone VARCHAR(20),
    address TEXT,
    status ENUM('Active', 'Inactive') NOT NULL DEFAULT 'Active',
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE rooms (
    room_id INT AUTO_INCREMENT PRIMARY KEY,
    room_number VARCHAR(20) NOT NULL UNIQUE,    -- e.g. "A-101"
    building VARCHAR(50),                        -- e.g. "Block A"
    room_type ENUM('Single', 'Double', 'Triple') NOT NULL DEFAULT 'Single',
    capacity INT NOT NULL DEFAULT 1,
    room_fee DECIMAL(10,2) NOT NULL DEFAULT 0,
    status ENUM('Available', 'Full', 'Maintenance') NOT NULL DEFAULT 'Available'
);

CREATE TABLE room_allocations (
    allocation_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    room_id INT NOT NULL,
    allocation_date DATE NOT NULL,
    checkout_date DATE NULL,                     -- NULL means "still living there"
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES rooms(room_id)
);

CREATE TABLE fees (
    fee_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    due_date DATE NOT NULL,
    payment_date DATE NULL,
    status ENUM('Pending', 'Paid', 'Overdue') NOT NULL DEFAULT 'Pending',
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

CREATE TABLE complaints (
    complaint_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    subject VARCHAR(200) NOT NULL,
    description TEXT,
    status ENUM('Submitted', 'In Progress', 'Resolved') NOT NULL DEFAULT 'Submitted',
    complaint_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

CREATE TABLE visitors (
    visitor_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    visitor_name VARCHAR(100) NOT NULL,
    relation VARCHAR(50),                        -- e.g. "Brother" (the frontend calls it relation)
    phone VARCHAR(20),
    visit_date DATE NOT NULL,
    check_in TIME NOT NULL,
    check_out TIME NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

CREATE TABLE expenses (
    expense_id INT AUTO_INCREMENT PRIMARY KEY,
    expense_name VARCHAR(150) NOT NULL,          -- the frontend calls this "title"
    category VARCHAR(100),
    amount DECIMAL(10,2) NOT NULL,
    expense_date DATE NOT NULL,                  -- the frontend calls this "date"
    description TEXT                             -- the frontend calls this "notes"
);
