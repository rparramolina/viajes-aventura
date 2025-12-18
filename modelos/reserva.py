from datetime import datetime

class Reserva:
    def __init__(self, id_reserva, usuario_id, paquete_id, fecha_reserva=None, estado='confirmada'):
        self.id_reserva = id_reserva
        self.usuario_id = usuario_id
        self.paquete_id = paquete_id
        self.fecha_reserva = fecha_reserva or datetime.now()
        self.estado = estado

    def __str__(self):
        return f"Reserva(id={self.id_reserva}, usuario_id={self.usuario_id}, paquete_id={self.paquete_id}, estado={self.estado})"
