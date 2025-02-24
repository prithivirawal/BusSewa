-- Create the database
CREATE DATABASE IF NOT EXISTS bus_sewa;
USE bus_sewa;

-- Create users table (for login/signup)
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(15),
    is_admin BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE
);

-- Create buses table (for admin to manage buses)
CREATE TABLE buses (
    bus_id INT AUTO_INCREMENT PRIMARY KEY,
    bus_number VARCHAR(20) UNIQUE NOT NULL,
    bus_name VARCHAR(100) NOT NULL,
    bus_type ENUM('AC', 'Non-AC') NOT NULL,
    total_seats INT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE
);

-- Create routes table (for admin to manage routes)
CREATE TABLE routes (
    route_id INT AUTO_INCREMENT PRIMARY KEY,
    source_city VARCHAR(100) NOT NULL,
    destination_city VARCHAR(100) NOT NULL,
    fare DECIMAL(10,2) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    UNIQUE KEY unique_route (source_city, destination_city)
);

-- Create schedules table (for showing available buses)
CREATE TABLE schedules (
    schedule_id INT AUTO_INCREMENT PRIMARY KEY,
    bus_id INT,
    route_id INT,
    departure_date DATE NOT NULL,
    departure_time TIME NOT NULL,
    available_seats INT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (bus_id) REFERENCES buses(bus_id),
    FOREIGN KEY (route_id) REFERENCES routes(route_id)
);

-- Create bookings table (for user bookings)
CREATE TABLE IF NOT EXISTS bookings (
    booking_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    schedule_id INT NOT NULL,
    booking_date DATE NOT NULL,
    passenger_name VARCHAR(100) NOT NULL,
    passenger_phone VARCHAR(15) NOT NULL,
    number_of_seats INT NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    seat_number INT NOT NULL,
    cancellation_reason VARCHAR(100),
    cancellation_date DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'Confirmed',
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (schedule_id) REFERENCES schedules(schedule_id)
);

-- Create simplified cities table
CREATE TABLE cities (
    city_id INT AUTO_INCREMENT PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL UNIQUE,
    is_active BOOLEAN DEFAULT TRUE
);

-- Insert initial cities
INSERT INTO cities (city_name) VALUES 
    ('Kathmandu'),
    ('Pokhara'),
    ('Chitwan'),
    ('Butwal'),
    ('Biratnagar'),
    ('Birgunj'),
    ('Dharan'),
    ('Nepalgunj'),
    ('Bhaktapur'),
    ('Lalitpur'),
    ('Dhangadhi'),
    ('Janakpur'),
    ('Hetauda'),
    ('Itahari'),
    ('Bharatpur');

-- Add admin user
INSERT INTO users (username, password, full_name, email, is_admin) 
VALUES ('admin', 'admin123', 'System Admin', 'admin@bussewa.com', TRUE);

-- Add some sample data
INSERT INTO buses (bus_number, bus_name, bus_type, total_seats) 
VALUES 
('BA 1 KHA 1234', 'Sajha Yatayat', 'AC', 40),
('BA 2 KHA 5678', 'Nepal Yatayat', 'Non-AC', 40);

INSERT INTO routes (source_city, destination_city, fare) 
VALUES 
('Kathmandu', 'Pokhara', 1000),
('Kathmandu', 'Chitwan', 800);

-- You might want to add these buses if they don't exist
INSERT INTO buses (bus_number, bus_name, bus_type, total_seats, is_active) 
VALUES 
    ('PY001', 'Prithivi Yatayat', 'AC', 40, TRUE),
    ('PY002', 'Prithivi Yatayat', 'Non-AC', 45, TRUE),
    ('SY001', 'Saugat Yatayat', 'AC', 40, TRUE),
    ('SY002', 'Saugat Yatayat', 'Non-AC', 45, TRUE),
    ('SPY001', 'Super Yatayat', 'AC', 40, TRUE),
    ('SPY002', 'Super Yatayat', 'Non-AC', 45, TRUE);

ALTER TABLE bookings
ADD COLUMN IF NOT EXISTS seat_number VARCHAR(10) DEFAULT NULL;

-- Modify the bookings table to ensure total_amount has proper type and default
ALTER TABLE bookings MODIFY COLUMN total_amount DECIMAL(10,2) NOT NULL DEFAULT 0.00;

-- Make sure all required columns are properly set
ALTER TABLE bookings 
    MODIFY COLUMN user_id INT NOT NULL,
    MODIFY COLUMN schedule_id INT NOT NULL,
    MODIFY COLUMN booking_date DATE NOT NULL,
    MODIFY COLUMN passenger_name VARCHAR(100) NOT NULL,
    MODIFY COLUMN passenger_phone VARCHAR(15) NOT NULL,
    MODIFY COLUMN number_of_seats INT NOT NULL,
    MODIFY COLUMN status VARCHAR(20) NOT NULL DEFAULT 'Confirmed';

-- Add necessary columns to bookings table if they don't exist
ALTER TABLE bookings
ADD COLUMN IF NOT EXISTS cancellation_reason VARCHAR(100),
ADD COLUMN IF NOT EXISTS cancellation_date DATE,
MODIFY COLUMN status VARCHAR(20) NOT NULL DEFAULT 'Confirmed',
MODIFY COLUMN total_amount DECIMAL(10,2) NOT NULL DEFAULT 0.00;

-- Create index for better search performance
CREATE INDEX IF NOT EXISTS idx_passenger_search 
ON bookings(passenger_name, passenger_phone);

-- Create index for date filtering
CREATE INDEX IF NOT EXISTS idx_departure_date 
ON schedules(departure_date);

-- Update the schedules table to track available seats
ALTER TABLE schedules
ADD COLUMN IF NOT EXISTS available_seats INT DEFAULT NULL;

-- Update buses table to store total seats
ALTER TABLE buses
ADD COLUMN IF NOT EXISTS total_seats INT DEFAULT 40;

-- Initialize available seats if NULL
UPDATE schedules s
JOIN buses b ON s.bus_id = b.bus_id
SET s.available_seats = b.total_seats
WHERE s.available_seats IS NULL; 