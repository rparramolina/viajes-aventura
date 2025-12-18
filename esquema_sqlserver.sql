-- Esquema de base de datos para Viajes Aventura (SQL Server)

-- Tabla de Usuarios
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[usuarios]') AND type in (N'U'))
BEGIN
    CREATE TABLE usuarios (
        id INT IDENTITY(1,1) PRIMARY KEY,
        nombre NVARCHAR(100) NOT NULL,
        email NVARCHAR(100) UNIQUE NOT NULL,
        password_hash NVARCHAR(255) NOT NULL,
        es_admin BIT DEFAULT 0
    );
END

-- Tabla de Destinos
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[destinos]') AND type in (N'U'))
BEGIN
    CREATE TABLE destinos (
        id INT IDENTITY(1,1) PRIMARY KEY,
        nombre NVARCHAR(100) NOT NULL,
        descripcion NVARCHAR(MAX),
        actividades NVARCHAR(MAX),
        costo_base DECIMAL(10, 2) NOT NULL
    );
END

-- Tabla de Paquetes Turísticos
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[paquetes]') AND type in (N'U'))
BEGIN
    CREATE TABLE paquetes (
        id INT IDENTITY(1,1) PRIMARY KEY,
        nombre NVARCHAR(100) NOT NULL,
        fecha_inicio DATE NOT NULL,
        fecha_fin DATE NOT NULL,
        precio_total DECIMAL(10, 2) NOT NULL
    );
END

-- Tabla Intermedia Paquetes - Destinos
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[paquete_destinos]') AND type in (N'U'))
BEGIN
    CREATE TABLE paquete_destinos (
        paquete_id INT REFERENCES paquetes(id) ON DELETE CASCADE,
        destino_id INT REFERENCES destinos(id) ON DELETE CASCADE,
        PRIMARY KEY (paquete_id, destino_id)
    );
END

-- Tabla de Reservas
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[reservas]') AND type in (N'U'))
BEGIN
    CREATE TABLE reservas (
        id INT IDENTITY(1,1) PRIMARY KEY,
        usuario_id INT REFERENCES usuarios(id) ON DELETE CASCADE,
        paquete_id INT REFERENCES paquetes(id) ON DELETE CASCADE,
        fecha_reserva DATETIME DEFAULT GETDATE(),
        estado NVARCHAR(50) DEFAULT 'confirmada'
    );
END
