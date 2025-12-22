from decimal import Decimal
from config.database import ConexionBD
from modelos.paquete import PaqueteTuristico
from repositorios.destino_repository import RepositorioDestino
import oracledb

class RepositorioPaquete:
    def __init__(self):
        self.bd = ConexionBD()
        self.repo_destino = RepositorioDestino()

    def guardar(self, paquete):
        cursor = self.bd.obtener_cursor()
        if not cursor:
            return None
        
        if paquete.destinos:
            # Requisitos: Precio basado en destinos y fechas (duración)
            costo_destinos = sum(Decimal(str(d.costo_base)) for d in paquete.destinos)
            costo_diario = Decimal('50.0')  # Factor de servicios por día
            duracion = Decimal(str(paquete.duracion_dias))
            paquete.precio_total = costo_destinos + (costo_diario * duracion)

        if paquete.id_paquete:
            # Update
            sql_update = """
                UPDATE paquetes SET nombre=:1, fecha_inicio=:2, fecha_fin=:3, precio_total=:4
                WHERE id=:5
            """
            valores = (paquete.nombre, paquete.fecha_inicio, paquete.fecha_fin, paquete.precio_total, paquete.id_paquete)
            try:
                cursor.execute(sql_update, valores)
                # Actualizar destinos: Borramos y reinsertamos relaciones (enfoque simple)
                cursor.execute("DELETE FROM paquete_destinos WHERE paquete_id=:1", (paquete.id_paquete,))
                for destino in paquete.destinos:
                    cursor.execute("INSERT INTO paquete_destinos (paquete_id, destino_id) VALUES (:1, :2)", 
                                (paquete.id_paquete, destino.id_destino))
                self.bd.conexion.commit()
                return paquete
            except Exception as e:
                self.bd.conexion.rollback()
                print(f"Error al actualizar paquete: {e}")
                return None
        else:
            # Insert (Oracle specific)
            sql_insert = """
                INSERT INTO paquetes (nombre, fecha_inicio, fecha_fin, precio_total)
                VALUES (:1, :2, :3, :4)
                RETURNING id INTO :5
            """
            valores = (paquete.nombre, paquete.fecha_inicio, paquete.fecha_fin, paquete.precio_total)
            try:
                id_variable = cursor.var(oracledb.NUMBER)
                cursor.execute(sql_insert, (*valores, id_variable))
                paquete.id_paquete = id_variable.getvalue()[0]
                
                for destino in paquete.destinos:
                    cursor.execute("INSERT INTO paquete_destinos (paquete_id, destino_id) VALUES (:1, :2)", 
                                (paquete.id_paquete, destino.id_destino))
                
                self.bd.conexion.commit()
                return paquete
            except Exception as e:
                self.bd.conexion.rollback()
                print(f"Error al crear paquete: {e}")
                return None

    def obtener_todos(self):
        cursor = self.bd.obtener_cursor()
        if not cursor:
            return []
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
        if not cursor:
            return None
        cursor.execute("SELECT id, nombre, fecha_inicio, fecha_fin, precio_total FROM paquetes WHERE id = :1", (id_paquete,))
        fila = cursor.fetchone()
        if fila:
            paquete = PaqueteTuristico(*fila)
            paquete.destinos = self._obtener_destinos_por_paquete(paquete.id_paquete)
            return paquete
        return None

    def _obtener_destinos_por_paquete(self, paquete_id):
        cursor = self.bd.obtener_cursor()
        if not cursor:
            return []
        sql = """
            SELECT d.id, d.nombre, d.descripcion, d.actividades, d.costo_base
            FROM destinos d
            JOIN paquete_destinos pd ON d.id = pd.destino_id
            WHERE pd.paquete_id = :1
        """
        cursor.execute(sql, (paquete_id,))
        filas = cursor.fetchall()
        from modelos.destino import Destino 
        return [Destino(*f) for f in filas]

    def obtener_disponibles(self, fecha_inicio, fecha_fin):
        cursor = self.bd.obtener_cursor()
        if not cursor:
            return []
        sql = """
            SELECT id, nombre, fecha_inicio, fecha_fin, precio_total 
            FROM paquetes 
            WHERE fecha_inicio >= :1 AND fecha_fin <= :2
        """
        cursor.execute(sql, (fecha_inicio, fecha_fin))
        filas = cursor.fetchall()
        paquetes = []
        for fila in filas:
            paquete = PaqueteTuristico(*fila)
            paquete.destinos = self._obtener_destinos_por_paquete(paquete.id_paquete)
            paquetes.append(paquete)
        return paquetes

    def eliminar(self, id_paquete):
        cursor = self.bd.obtener_cursor()
        if not cursor:
            return False
        try:
            cursor.execute("DELETE FROM paquetes WHERE id = :1", (id_paquete,))
            self.bd.conexion.commit()
            return True
        except Exception as e:
            self.bd.conexion.rollback()
            print(f"Error al eliminar paquete: {e}")
            return False
