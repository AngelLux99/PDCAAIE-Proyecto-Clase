-- CREAR BASE DE DATOS
CREATE DATABASE Proyecto;

-- USAR BASE DE DATOS
USE Proyecto;

-- CREAR TABLA TIPO USUARIO
CREATE TABLE TipoUsuarios(
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL
);

-- CREAR TABLA USUARRIO
CREATE TABLE Usuarios(
    id SERIAL PRIMARY KEY,
    nombre_completo VARCHAR(100) NOT NULL,
    username VARCHAR(20) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    edad SMALLINT NOT NULL,
    fotografia VARCHAR(100) NOT NULL,
    contrasena VARCHAR(100) NOT NULL,
    intentos SMALLINT NOT NULL,
    tipoUsuarioId INTEGER NOT NULL,
    FOREIGN KEY (tipoUsuarioId) REFERENCES TipoUsuarios(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

-- CREAR TABLA BITACORA
CREATE TABLE Bitacoras(
    id SERIAL PRIMARY KEY,
    fecha_hora TIMESTAMP NOT NULL,
    usuarioId INTEGER NOT NULL,
    direccion_ip VARCHAR(15) NOT NULL,
    accion VARCHAR(500) NOT NULL,
    FOREIGN KEY (usuarioId) REFERENCES Usuarios(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);