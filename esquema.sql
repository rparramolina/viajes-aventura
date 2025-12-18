-- Esquema de base de datos para Viajes Aventura

-- Tabla de Usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    es_admin BOOLEAN DEFAULT FALSE
);

-- Tabla de Destinos
CREATE TABLE IF NOT EXISTS destinos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    actividades TEXT,
    costo_base DECIMAL(10, 2) NOT NULL
);

-- Tabla de Paquetes Turísticos
CREATE TABLE IF NOT EXISTS paquetes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    precio_total DECIMAL(10, 2) NOT NULL
);

-- Tabla Intermedia Paquetes - Destinos (Relación Muchos a Muchos)
CREATE TABLE IF NOT EXISTS paquete_destinos (
    paquete_id INTEGER REFERENCES paquetes(id) ON DELETE CASCADE,
    destino_id INTEGER REFERENCES destinos(id) ON DELETE CASCADE,
    PRIMARY KEY (paquete_id, destino_id)
);

-- Tabla de Reservas
CREATE TABLE IF NOT EXISTS reservas (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
    paquete_id INTEGER REFERENCES paquetes(id) ON DELETE CASCADE,
    fecha_reserva TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(50) DEFAULT 'confirmada'
);
