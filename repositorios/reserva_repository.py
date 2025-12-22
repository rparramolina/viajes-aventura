from config.database import ConexionBD
from modelos.reserva import Reserva
from config.settings import DB_ENGINE
from utils.sql_compat import query_compat

class RepositorioReserva:
    def __init__(self):
        self.bd = ConexionBD()

    def guardar(self, reserva):
        cursor = self.bd.obtener_cursor()
        if not cursor:
            return None

        if DB_ENGINE == "oracle":
            import oracledb
            sql = """
                INSERT INTO reservas (usuario_id, paquete_id, fecha_reserva, estado)
                VALUES (:1, :2, :3, :4)
                RETURNING id INTO :5
            """
            try:
                id_variable = cursor.var(oracledb.NUMBER)
                valores = (reserva.usuario_id, reserva.paquete_id, reserva.fecha_reserva, reserva.estado)
                cursor.execute(sql, (*valores, id_variable))
                reserva.id_reserva = id_variable.getvalue()[0]
                self.bd.conexion.commit()
                return reserva
            except Exception as e:
                self.bd.conexion.rollback()
                print(f"Error al guardar reserva (Oracle): {e}")
                return None

        sql = query_compat("""
            INSERT INTO reservas (usuario_id, paquete_id, fecha_reserva, estado)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """)
        try:
            cursor.execute(sql, (reserva.usuario_id, reserva.paquete_id, reserva.fecha_reserva, reserva.estado))
            reserva.id_reserva = cursor.fetchone()[0]
            self.bd.conexion.commit()
            return reserva
        except Exception as e:
            self.bd.conexion.rollback()
            print(f"Error al guardar reserva: {e}")
            return None

    def obtener_por_usuario(self, usuario_id):
        cursor = self.bd.obtener_cursor()
        if not cursor:
            return []
        sql = "SELECT id, usuario_id, paquete_id, fecha_reserva, estado FROM reservas WHERE usuario_id = %s"
        cursor.execute(query_compat(sql), (usuario_id,))
        filas = cursor.fetchall()
        return [Reserva(*f) for f in filas]
