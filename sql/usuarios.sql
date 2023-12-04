-- Crear la tabla de usuarios con información de autenticación
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    token TEXT
);

-- Insertar un usuario de ejemplo con un token
INSERT INTO users (username, password, token) VALUES ('admin', 'admin_password', '1234');
