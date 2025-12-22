# Diseño del Sistema - Viajes Aventura

Este documento contiene el diagrama de clases UML que representa la arquitectura del sistema, incluyendo modelos, repositorios y servicios.

## Diagrama de Clases

```mermaid
classDiagram
    direction TB

    class ConexionBD {
        -_instancia: ConexionBD
        +conexion: object
        +conectar()
        +cerrar()
        +obtener_cursor()
    }

    class Usuario {
        +id_usuario: int
        +nombre: str
        +email: str
        +password_hash: str
        +es_admin: bool
    }

    class Destino {
        +id_destino: int
        +nombre: str
        +descripcion: str
        +actividades: str
        +costo_base: float
    }

    class PaqueteTuristico {
        +id_paquete: int
        +nombre: str
        +fecha_inicio: date
        +fecha_fin: date
        +precio_total: float
        +destinos: List~Destino~
        +agregar_destino(destino)
        +duracion_dias() int
    }

    class Reserva {
        +id_reserva: int
        +usuario_id: int
        +paquete_id: int
        +fecha_reserva: datetime
        +estado: str
    }

    class RepositorioUsuario {
        +bd: ConexionBD
        +guardar(usuario)
        +obtener_por_email(email)
        +obtener_por_id(id)
    }

    class RepositorioDestino {
        +bd: ConexionBD
        +guardar(destino)
        +obtener_todos()
        +obtener_por_id(id)
        +eliminar(id)
    }

    class RepositorioPaquete {
        +bd: ConexionBD
        +guardar(paquete)
        +obtener_todos()
        +obtener_por_id(id)
        +eliminar(id)
    }

    class RepositorioReserva {
        +bd: ConexionBD
        +guardar(reserva)
        +obtener_por_usuario(usuario_id)
    }

    class ServicioAutenticacion {
        +repo_usuario: RepositorioUsuario
        +usuario_actual: Usuario
        +registrar_usuario()
        +login()
        +logout()
        +esta_autenticado()
    }

    class GestorAdministracion {
        +repo_destino: RepositorioDestino
        +repo_paquete: RepositorioPaquete
        +crear_destino()
        +listar_destinos()
        +crear_paquete()
    }

    class GestorReservas {
        +repo_reserva: RepositorioReserva
        +repo_paquete: RepositorioPaquete
        +crear_reserva()
        +listar_mis_reservas()
    }

    %% Relaciones de Modelos
    PaqueteTuristico "1" --> "*" Destino : contiene
    Reserva "*" --> "1" Usuario : pertenece a
    Reserva "*" --> "1" PaqueteTuristico : reserva

    %% Relaciones de Repositorios (Uso de BD)
    RepositorioUsuario ..> ConexionBD
    RepositorioDestino ..> ConexionBD
    RepositorioPaquete ..> ConexionBD
    RepositorioReserva ..> ConexionBD

    %% Relaciones de Servicios (Uso de Repositorios)
    ServicioAutenticacion --> RepositorioUsuario
    GestorAdministracion --> RepositorioDestino
    GestorAdministracion --> RepositorioPaquete
    GestorReservas --> RepositorioReserva
    GestorReservas --> RepositorioPaquete
```
