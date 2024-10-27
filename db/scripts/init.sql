CREATE DATABASE news_app_db;

\c news_app_db;

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,  
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL
);

CREATE TABLE IF NOT EXISTS news_topic (
  id SERIAL PRIMARY KEY,
  topics TEXT[] NOT NULL,
  user_id INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- INSERT INTO users (username, email, password) VALUES 
--     ('admin', 'admin@g.com', 'admin'), 
--     ('john_doe', 'john@example.com', 'john123'), 
--     ('jane_doe', 'janedoe@gmail.com', 'jane123');
