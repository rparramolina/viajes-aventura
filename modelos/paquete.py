from datetime import date

class PaqueteTuristico:
    def __init__(self, id_paquete, nombre, fecha_inicio, fecha_fin, precio_total=0.0):
        self.id_paquete = id_paquete
        self.nombre = nombre
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.precio_total = precio_total
        self.destinos = []  # Lista de objetos Destino

    def agregar_destino(self, destino):
        self.destinos.append(destino)
        

    @property
    def duracion_dias(self):
        if isinstance(self.fecha_inicio, date) and isinstance(self.fecha_fin, date):
            delta = self.fecha_fin - self.fecha_inicio
            return delta.days
        return 0

    def __str__(self):
        return f"Paquete(id={self.id_paquete}, nombre={self.nombre}, precio={self.precio_total})"
