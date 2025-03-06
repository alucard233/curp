-- Crear la base de datos
CREATE DATABASE mexico;

-- Conectar a la base de datos (dependiendo del cliente SQL, esto puede variar)
\c mexico;

-- Crear la tabla curp
CREATE TABLE curp (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(100) NOT NULL,
    apellido_materno VARCHAR(100),
    fecha_nacimiento VARCHAR(10) NOT NULL,
    genero CHAR(1) NOT NULL,
    estado_nacimiento VARCHAR(50) NOT NULL,
    curp VARCHAR(18) NOT NULL UNIQUE
);
