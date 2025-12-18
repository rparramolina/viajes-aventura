from repositorios.reserva_repository import RepositorioReserva
from repositorios.paquete_repository import RepositorioPaquete
from modelos.reserva import Reserva

class GestorReservas:
    def __init__(self):
        self.repo_reserva = RepositorioReserva()
        self.repo_paquete = RepositorioPaquete()

    def crear_reserva(self, usuario, paquete_id):
        if not usuario:
            raise Exception("Debe estar autenticado para reservar.")
        
        paquete = self.repo_paquete.obtener_por_id(paquete_id)
        if not paquete:
            raise Exception("Paquete no encontrado.")

        reserva = Reserva(None, usuario.id_usuario, paquete.id_paquete)
        return self.repo_reserva.guardar(reserva)

    def listar_mis_reservas(self, usuario):
        if not usuario:
            raise Exception("Usuario no válido.")
        return self.repo_reserva.obtener_por_usuario(usuario.id_usuario)
