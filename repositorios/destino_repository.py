from config.database import ConexionBD
from modelos.destino import Destino

class RepositorioDestino:
    def __init__(self):
        self.bd = ConexionBD()

    def guardar(self, destino):
        cursor = self.bd.obtener_cursor()
        if destino.id_destino:
            # Actualizar
            sql = """
                UPDATE destinos SET nombre=%s, descripcion=%s, actividades=%s, costo_base=%s
                WHERE id=%s
            """
            valores = (destino.nombre, destino.descripcion, destino.actividades, destino.costo_base, destino.id_destino)
        else:
            # Insertar
            sql = """
                INSERT INTO destinos (nombre, descripcion, actividades, costo_base)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """
            valores = (destino.nombre, destino.descripcion, destino.actividades, destino.costo_base)

        try:
            cursor.execute(sql, valores)
            if not destino.id_destino:
                destino.id_destino = cursor.fetchone()[0]
            self.bd.conexion.commit()
            return destino
        except Exception as e:
            self.bd.conexion.rollback()
            print(f"Error al guardar destino: {e}")
            return None

    def obtener_todos(self):
        cursor = self.bd.obtener_cursor()
        cursor.execute("SELECT id, nombre, descripcion, actividades, costo_base FROM destinos")
        filas = cursor.fetchall()
        return [Destino(*fila) for fila in filas]

    def obtener_por_id(self, id_destino):
        cursor = self.bd.obtener_cursor()
        cursor.execute("SELECT id, nombre, descripcion, actividades, costo_base FROM destinos WHERE id = %s", (id_destino,))
        resultado = cursor.fetchone()
        if resultado:
            return Destino(*resultado)
        return None

    def eliminar(self, id_destino):
        cursor = self.bd.obtener_cursor()
        try:
            cursor.execute("DELETE FROM destinos WHERE id = %s", (id_destino,))
            self.bd.conexion.commit()
            return True
        except Exception as e:
            self.bd.conexion.rollback()
            print(f"Error al eliminar destino: {e}")
            return False
