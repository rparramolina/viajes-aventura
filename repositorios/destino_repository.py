from config.database import ConexionBD
from modelos.destino import Destino
import oracledb

class RepositorioDestino:
    def __init__(self):
        self.bd = ConexionBD()

    def guardar(self, destino):
        cursor = self.bd.obtener_cursor()
        if not cursor:
            return None
        
        if destino.id_destino:
            # Actualizar
            sql = """
                UPDATE destinos SET nombre=:1, descripcion=:2, actividades=:3, costo_base=:4
                WHERE id=:5
            """
            valores = (destino.nombre, destino.descripcion, destino.actividades, destino.costo_base, destino.id_destino)
            try:
                cursor.execute(sql, valores)
                self.bd.conexion.commit()
                return destino
            except Exception as e:
                self.bd.conexion.rollback()
                print(f"Error al actualizar destino: {e}")
                return None
        else:
            # Insertar (Oracle specific)
            sql = """
                INSERT INTO destinos (nombre, descripcion, actividades, costo_base)
                VALUES (:1, :2, :3, :4)
                RETURNING id INTO :5
            """
            valores = (destino.nombre, destino.descripcion, destino.actividades, destino.costo_base)
            try:
                id_variable = cursor.var(oracledb.NUMBER)
                cursor.execute(sql, (*valores, id_variable))
                destino.id_destino = id_variable.getvalue()[0]
                self.bd.conexion.commit()
                return destino
            except Exception as e:
                self.bd.conexion.rollback()
                print(f"Error al guardar destino: {e}")
                return None

    def obtener_todos(self):
        cursor = self.bd.obtener_cursor()
        if not cursor:
            return []
        cursor.execute("SELECT id, nombre, descripcion, actividades, costo_base FROM destinos")
        filas = cursor.fetchall()
        return [Destino(*fila) for fila in filas]

    def obtener_por_id(self, id_destino):
        cursor = self.bd.obtener_cursor()
        if not cursor:
            return None
        cursor.execute("SELECT id, nombre, descripcion, actividades, costo_base FROM destinos WHERE id = :1", (id_destino,))
        resultado = cursor.fetchone()
        if resultado:
            return Destino(*resultado)
        return None

    def eliminar(self, id_destino):
        cursor = self.bd.obtener_cursor()
        if not cursor:
            return False
        try:
            cursor.execute("DELETE FROM destinos WHERE id = :1", (id_destino,))
            self.bd.conexion.commit()
            return True
        except Exception as e:
            self.bd.conexion.rollback()
            print(f"Error al eliminar destino: {e}")
            return False
