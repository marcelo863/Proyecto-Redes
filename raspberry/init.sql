CREATE DATABASE IF NOT EXISTS redesDB;
USE redesDB;
CREATE TABLE IF NOT EXISTS registro
    (id INTEGER PRIMARY KEY,
    hora DATETIME,
    reconocimiento INT,
    prob_reconocimiento DECIMAL);
