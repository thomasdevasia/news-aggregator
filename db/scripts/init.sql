CREATE DATABASE news_app_db;

\c news_app_db;

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,  
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL
);

-- INSERT INTO users (username, email, password) VALUES 
--     ('admin', 'admin@g.com', 'admin'), 
--     ('john_doe', 'john@example.com', 'john123'), 
--     ('jane_doe', 'janedoe@gmail.com', 'jane123');