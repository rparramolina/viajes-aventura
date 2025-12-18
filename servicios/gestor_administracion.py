from repositorios.destino_repository import RepositorioDestino
from repositorios.paquete_repository import RepositorioPaquete
from modelos.destino import Destino
from modelos.paquete import PaqueteTuristico

class GestorAdministracion:
    def __init__(self):
        self.repo_destino = RepositorioDestino()
        self.repo_paquete = RepositorioPaquete()

    def crear_destino(self, nombre, descripcion, actividades, costo_base):
        destino = Destino(None, nombre, descripcion, actividades, costo_base)
        return self.repo_destino.guardar(destino)

    def listar_destinos(self):
        return self.repo_destino.obtener_todos()

    def eliminar_destino(self, id_destino):
        return self.repo_destino.eliminar(id_destino)

    def crear_paquete(self, nombre, fecha_inicio, fecha_fin, destinos_ids):
        # Primero recuperamos los objetos destino
        destinos = []
        for d_id in destinos_ids:
            d = self.repo_destino.obtener_por_id(d_id)
            if d:
                destinos.append(d)
        
        paquete = PaqueteTuristico(None, nombre, fecha_inicio, fecha_fin)
        paquete.destinos = destinos
        
        return self.repo_paquete.guardar(paquete)

    def listar_paquetes(self):
        return self.repo_paquete.obtener_todos()
