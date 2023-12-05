-- Crear la tabla de usuarios con información de autenticación
CREATE TABLE IF NOT EXISTS usuarios (
    username VARCHAR (100) PRIMARY KEY NOT NULL,
    password VARCHAR (32) NOT NULL,
    token VARCHAR(65) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- password 123456789
INSERT INTO usuarios (username, password, token) VALUES ('usuario@email.com', '25f9e794323b453885f5181f1b624d0b', '1234');
