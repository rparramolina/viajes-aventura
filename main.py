import sys
from servicios.autenticacion import ServicioAutenticacion
from servicios.gestor_administracion import GestorAdministracion
from servicios.gestor_reservas import GestorReservas
from datetime import date

class Aplicacion:
    def __init__(self):
        self.auth = ServicioAutenticacion()
        self.admin = GestorAdministracion()
        self.reservas = GestorReservas()

    def mostrar_menu_principal(self):
        print("\n--- VIAJES AVENTURA ---")
        if self.auth.esta_autenticado():
            usuario = self.auth.usuario_actual
            print(f"Bienvenido, {usuario.nombre} ({'Admin' if usuario.es_admin else 'Cliente'})")
            if usuario.es_admin:
                print("1. Gestionar Destinos")
                print("2. Gestionar Paquetes")
            print("3. Ver Paquetes Disponibles")
            print("4. Reservar Paquete")
            print("5. Mis Reservas")
            print("0. Cerrar Sesión")
        else:
            print("1. Iniciar Sesión")
            print("2. Registrarse")
            print("0. Salir")

    def ejecutar(self):
        while True:
            self.mostrar_menu_principal()
            opcion = input("Seleccione una opción: ")

            if not self.auth.esta_autenticado():
                if opcion == "1":
                    self.login()
                elif opcion == "2":
                    self.registro()
                elif opcion == "0":
                    print("¡Hasta luego!")
                    break
                else:
                    print("Opción inválida.")
            else:
                if self.auth.es_admin():
                    if opcion == "1":
                        self.menu_destinos()
                    elif opcion == "2":
                        self.menu_paquetes()
                    elif opcion == "3":
                        self.listar_paquetes()
                    elif opcion == "4":
                        self.reservar()
                    elif opcion == "5":
                        self.mis_reservas()
                    elif opcion == "0":
                        self.auth.logout()
                    else:
                        print("Opción inválida.")
                else:
                    if opcion == "3":
                        self.listar_paquetes()
                    elif opcion == "4":
                        self.reservar()
                    elif opcion == "5":
                        self.mis_reservas()
                    elif opcion == "0":
                        self.auth.logout()
                    else:
                        print("Opción inválida.")

    def login(self):
        email = input("Email: ")
        password = input("Contraseña: ")
        usuario = self.auth.login(email, password)
        if usuario:
            print("Login exitoso.")
        else:
            print("Credenciales incorrectas.")

    def registro(self):
        nombre = input("Nombre: ")
        email = input("Email: ")
        password = input("Contraseña: ")
        es_admin_input = input("¿Es administrador? (s/n): ")
        es_admin = es_admin_input.lower() == 's'
        try:
            self.auth.registrar_usuario(nombre, email, password, es_admin)
            print("Usuario registrado exitosamente.")
        except Exception as e:
            print(f"Error al registrar: {e}")

    def menu_destinos(self):
        print("\n--- GESTIÓN DE DESTINOS ---")
        print("1. Crear Destino")
        print("2. Listar Destinos")
        print("0. Volver")
        opcion = input("Opción: ")
        if opcion == "1":
            nombre = input("Nombre: ")
            desc = input("Descripción: ")
            act = input("Actividades: ")
            costo = float(input("Costo Base: "))
            self.admin.crear_destino(nombre, desc, act, costo)
            print("Destino creado.")
        elif opcion == "2":
            destinos = self.admin.listar_destinos()
            for d in destinos:
                print(d)
    
    def menu_paquetes(self):
        print("\n--- GESTIÓN DE PAQUETES ---")
        print("1. Crear Paquete")
        print("2. Listar Paquetes")
        print("0. Volver")
        opcion = input("Opción: ")
        if opcion == "1":
            nombre = input("Nombre: ")
            f_inicio = input("Fecha Inicio (YYYY-MM-DD): ")
            f_fin = input("Fecha Fin (YYYY-MM-DD): ")
            # Listar destinos para seleccionar
            destinos = self.admin.listar_destinos()
            for d in destinos:
                print(f"{d.id_destino}: {d.nombre}")
            ids = input("IDs de destinos (separados por coma): ")
            destinos_ids = [int(i.strip()) for i in ids.split(',')]
            
            self.admin.crear_paquete(nombre, date.fromisoformat(f_inicio), date.fromisoformat(f_fin), destinos_ids)
            print("Paquete creado.")
        elif opcion == "2":
            self.listar_paquetes()

    def listar_paquetes(self):
        paquetes = self.admin.listar_paquetes()
        print("\n--- PAQUETES DISPONIBLES ---")
        for p in paquetes:
            print(p)
            print("  Destinos:")
            for d in p.destinos:
                print(f"   - {d.nombre} ({d.actividades})")

    def reservar(self):
        id_paquete = input("ID del Paquete a reservar: ")
        try:
            reserva = self.reservas.crear_reserva(self.auth.usuario_actual, int(id_paquete))
            if reserva:
                print(f"Reserva creada con ID: {reserva.id_reserva}")
        except Exception as e:
            print(f"Error al reservar: {e}")

    def mis_reservas(self):
        mis_r = self.reservas.listar_mis_reservas(self.auth.usuario_actual)
        print("\n--- MIS RESERVAS ---")
        for r in mis_r:
            print(r)

if __name__ == "__main__":
    app = Aplicacion()
    app.ejecutar()
