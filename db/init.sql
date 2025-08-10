CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100)
);

INSERT INTO usuarios (nombre, email) VALUES ('Sergio', 'sergio@example.com');

CREATE TABLE IF NOT EXISTS video_tasks (
    task_id VARCHAR(50) PRIMARY KEY,
    video_url TEXT NOT NULL,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);