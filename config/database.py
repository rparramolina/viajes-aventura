from config.settings import (
    DB_ENGINE, DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT,
    SQL_SERVER, SQL_DATABASE, SQL_USER, SQL_PASS, SQL_DRIVER
)

class ConexionBD:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(ConexionBD, cls).__new__(cls)
            cls._instancia.conexion = None
        return cls._instancia

    def conectar(self):
        if self.conexion is None or (hasattr(self.conexion, 'closed') and self.conexion.closed):
            try:
                if DB_ENGINE == "sqlserver":
                    import pyodbc
                    conn_str = f'DRIVER={SQL_DRIVER};SERVER={SQL_SERVER};DATABASE={SQL_DATABASE};UID={SQL_USER};PWD={SQL_PASS}'
                    self.conexion = pyodbc.connect(conn_str)
                    print("Conexión a SQL Server establecida exitosamente.")
                else:
                    import psycopg2
                    self.conexion = psycopg2.connect(
                        host=DB_HOST,
                        database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        port=DB_PORT
                    )
                    print("Conexión a PostgreSQL establecida exitosamente.")
            except Exception as e:
                print(f"Error al conectar a la base de datos: {e}")
                self.conexion = None
        return self.conexion

    def cerrar(self):
        if self.conexion and not self.conexion.closed:
            self.conexion.close()
            print("Conexión a base de datos cerrada.")

    def obtener_cursor(self):
        if self.conexion is None or self.conexion.closed:
            self.conectar()
        if self.conexion:
            return self.conexion.cursor()
        return None
