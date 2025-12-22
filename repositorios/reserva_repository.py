from config.database import ConexionBD
from modelos.reserva import Reserva
import oracledb

class RepositorioReserva:
    def __init__(self):
        self.bd = ConexionBD()

    def guardar(self, reserva):
        cursor = self.bd.obtener_cursor()
        if not cursor:
            return None

        # Insertar (Oracle specific)
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
            print(f"Error al guardar reserva: {e}")
            return None

    def obtener_por_usuario(self, usuario_id):
        cursor = self.bd.obtener_cursor()
        if not cursor:
            return []
        sql = "SELECT id, usuario_id, paquete_id, fecha_reserva, estado FROM reservas WHERE usuario_id = :1"
        cursor.execute(sql, (usuario_id,))
        filas = cursor.fetchall()
        return [Reserva(*f) for f in filas]
