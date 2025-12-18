from config.database import ConexionBD
from modelos.paquete import PaqueteTuristico
from repositorios.destino_repository import RepositorioDestino

class RepositorioPaquete:
    def __init__(self):
        self.bd = ConexionBD()
        self.repo_destino = RepositorioDestino()

    def guardar(self, paquete):
        cursor = self.bd.obtener_cursor()
        
        if paquete.precio_total == 0 and paquete.destinos:
            paquete.precio_total = sum(d.costo_base for d in paquete.destinos)

        if paquete.id_paquete:
            # Update
            sql_update = """
                UPDATE paquetes SET nombre=%s, fecha_inicio=%s, fecha_fin=%s, precio_total=%s
                WHERE id=%s
            """
            valores = (paquete.nombre, paquete.fecha_inicio, paquete.fecha_fin, paquete.precio_total, paquete.id_paquete)
            try:
                cursor.execute(sql_update, valores)
                # Actualizar destinos: Borramos y reinsertamos relaciones (enfoque simple)
                cursor.execute("DELETE FROM paquete_destinos WHERE paquete_id=%s", (paquete.id_paquete,))
                for destino in paquete.destinos:
                    cursor.execute("INSERT INTO paquete_destinos (paquete_id, destino_id) VALUES (%s, %s)", 
                                (paquete.id_paquete, destino.id_destino))
                self.bd.conexion.commit()
                return paquete
            except Exception as e:
                self.bd.conexion.rollback()
                print(f"Error al actualizar paquete: {e}")
                return None
        else:
            # Insert
            sql_insert = """
                INSERT INTO paquetes (nombre, fecha_inicio, fecha_fin, precio_total)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """
            valores = (paquete.nombre, paquete.fecha_inicio, paquete.fecha_fin, paquete.precio_total)
            try:
                cursor.execute(sql_insert, valores)
                paquete.id_paquete = cursor.fetchone()[0]
                
                for destino in paquete.destinos:
                    cursor.execute("INSERT INTO paquete_destinos (paquete_id, destino_id) VALUES (%s, %s)", 
                                (paquete.id_paquete, destino.id_destino))
                
                self.bd.conexion.commit()
                return paquete
            except Exception as e:
                self.bd.conexion.rollback()
                print(f"Error al crear paquete: {e}")
                return None

    def obtener_todos(self):
        cursor = self.bd.obtener_cursor()
        cursor.execute("SELECT id, nombre, fecha_inicio, fecha_fin, precio_total FROM paquetes")
        filas = cursor.fetchall()
        paquetes = []
        for fila in filas:
            paquete = PaqueteTuristico(*fila)
            paquete.destinos = self._obtener_destinos_por_paquete(paquete.id_paquete)
            paquetes.append(paquete)
        return paquetes

    def obtener_por_id(self, id_paquete):
        cursor = self.bd.obtener_cursor()
        cursor.execute("SELECT id, nombre, fecha_inicio, fecha_fin, precio_total FROM paquetes WHERE id = %s", (id_paquete,))
        fila = cursor.fetchone()
        if fila:
            paquete = PaqueteTuristico(*fila)
            paquete.destinos = self._obtener_destinos_por_paquete(paquete.id_paquete)
            return paquete
        return None

    def _obtener_destinos_por_paquete(self, paquete_id):
        cursor = self.bd.obtener_cursor()
        sql = """
            SELECT d.id, d.nombre, d.descripcion, d.actividades, d.costo_base
            FROM destinos d
            JOIN paquete_destinos pd ON d.id = pd.destino_id
            WHERE pd.paquete_id = %s
        """
        cursor.execute(sql, (paquete_id,))
        filas = cursor.fetchall()
        # Importamos Destino aquí o usamos los datos crudos, idealmente usamos modelo
        from modelos.destino import Destino 
        return [Destino(*f) for f in filas]

    def eliminar(self, id_paquete):
        cursor = self.bd.obtener_cursor()
        try:
            cursor.execute("DELETE FROM paquetes WHERE id = %s", (id_paquete,))
            self.bd.conexion.commit()
            return True
        except Exception as e:
            self.bd.conexion.rollback()
            print(f"Error al eliminar paquete: {e}")
            return False
