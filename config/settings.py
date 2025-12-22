import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configuraciones de Base de Datos
DB_ENGINE = os.getenv("DB_ENGINE", "oracle")  # 'postgresql', 'sqlserver', 'oracle'

# PostgreSQL
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "viajes")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")

# SQL Server
SQL_SERVER = os.getenv("SQL_SERVER", "localhost")
SQL_DATABASE = os.getenv("SQL_DATABASE", "viajes")
SQL_USER = os.getenv("SQL_USER", "sa")
SQL_PASS = os.getenv("SQL_PASS", "Password123!")
SQL_DRIVER = os.getenv("SQL_DRIVER", "{ODBC Driver 17 for SQL Server}")

# Oracle
ORACLE_USER = os.getenv("ORACLE_USER", "system")
ORACLE_PASS = os.getenv("ORACLE_PASS", "oracle")
ORACLE_DSN = os.getenv("ORACLE_DSN", "localhost/xepdb1")

# Otras configuraciones
SECRET_KEY = os.getenv("SECRET_KEY", "super_secreto")
