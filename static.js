CREATE DATABASE agenda_db;

USE agenda_db;

CREATE TABLE contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100)
);

CREATE TABLE events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    contact_id INT,
    event_title VARCHAR(255),
    event_date DATE,
    event_time TIME,
    FOREIGN KEY (contact_id) REFERENCES contacts(id)
);
