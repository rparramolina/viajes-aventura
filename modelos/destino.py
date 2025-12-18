class Destino:
    def __init__(self, id_destino, nombre, descripcion, actividades, costo_base):
        self.id_destino = id_destino
        self.nombre = nombre
        self.descripcion = descripcion
        self.actividades = actividades
        self.costo_base = costo_base

    def __str__(self):
        return f"Destino(id={self.id_destino}, nombre={self.nombre}, costo={self.costo_base})"
