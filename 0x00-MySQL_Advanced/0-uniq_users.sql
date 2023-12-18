-- script that creates a table users
CREATE TABLE users (
       id INTEGER PRIMARY KEY NOT NULL AUTOINCREMENT,
       email VARCHAR(255),
       name VARCHAR(255)
) IF NOT EXISTS;
