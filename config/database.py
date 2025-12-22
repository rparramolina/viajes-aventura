from config.settings import ORACLE_USER, ORACLE_PASS, ORACLE_DSN

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
                import oracledb
                print(f"Intentando conectar a Oracle con usuario: {ORACLE_USER} a {ORACLE_DSN}")
                self.conexion = oracledb.connect(
                    user=ORACLE_USER,
                    password=ORACLE_PASS,
                    dsn=ORACLE_DSN
                )
                print("Conexión a Oracle establecida exitosamente.")
            except Exception as e:
                import traceback
                traceback.print_exc()
                print(f"Error al conectar a la base de datos Oracle: {e}")
                self.conexion = None
        return self.conexion

    def cerrar(self):
        if self.conexion:
            try:
                if hasattr(self.conexion, 'closed'):
                    if not self.conexion.closed:
                        self.conexion.close()
                        print("Conexión a base de datos cerrada.")
                else:
                    self.conexion.close()
                    print("Conexión a base de datos cerrada.")
            except Exception as e:
                print(f"Error al cerrar la conexión: {e}")

    def obtener_cursor(self):
        if self.conexion is None or (hasattr(self.conexion, 'closed') and self.conexion.closed):
            self.conectar()
        if self.conexion:
            return self.conexion.cursor()
        return None
