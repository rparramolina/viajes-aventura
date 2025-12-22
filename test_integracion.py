import unittest
from datetime import date, datetime
from servicios.autenticacion import ServicioAutenticacion
from servicios.gestor_administracion import GestorAdministracion
from servicios.gestor_reservas import GestorReservas
from modelos.usuario import Usuario

class TestIntegracionSistema(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.auth = ServicioAutenticacion()
        cls.admin = GestorAdministracion()
        cls.reservas = GestorReservas()
        
        # Datos de prueba
        cls.email_admin = f"admin_test_{datetime.now().timestamp()}@test.com"
        cls.email_cliente = f"cliente_test_{datetime.now().timestamp()}@test.com"
        cls.password = "password123"

    def test_01_flujo_usuarios(self):
        print("\nProbando flujo de usuarios...")
        # Registro Admin
        admin = self.auth.registrar_usuario("Admin Test", self.email_admin, self.password, es_admin=True)
        self.assertIsNotNone(admin.id_usuario)
        
        # Registro Cliente
        cliente = self.auth.registrar_usuario("Cliente Test", self.email_cliente, self.password, es_admin=False)
        self.assertIsNotNone(cliente.id_usuario)
        
        # Login
        user_logged = self.auth.login(self.email_admin, self.password)
        self.assertTrue(self.auth.esta_autenticado())
        self.assertTrue(user_logged.es_admin)

    def test_02_gestion_destinos(self):
        print("\nProbando gestión de destinos...")
        # Crear
        destino = self.admin.crear_destino("Paris", "Ciudad Luz", "Torre Eiffel", 500.0)
        self.assertIsNotNone(destino.id_destino)
        id_dest = destino.id_destino
        
        # Editar
        self.admin.editar_destino(id_dest, "Paris Editado", "Nueva Desc", "Nuevas Act", 600.0)
        dest_editado = self.admin.obtener_destino_por_id(id_dest)
        self.assertEqual(dest_editado.nombre, "Paris Editado")
        self.assertEqual(dest_editado.costo_base, 600.0)

    def test_03_gestion_paquetes(self):
        print("\nProbando gestión de paquetes y cálculo de precio...")
        # Crear destinos para el paquete
        d1 = self.admin.crear_destino("Roma", "Historia", "Coliseo", 300.0)
        d2 = self.admin.crear_destino("Madrid", "Cultura", "Prado", 200.0)
        
        # Crear paquete (5 días: de 1 a 6)
        f_inicio = date(2025, 5, 1)
        f_fin = date(2025, 5, 6)
        paquete = self.admin.crear_paquete("EuroTour", f_inicio, f_fin, [d1.id_destino, d2.id_destino])
        
        # Verificar precio: 300 (d1) + 200 (d2) + (50 * 5 días) = 750.0
        self.assertEqual(float(paquete.precio_total), 750.0)
        
        # Búsqueda por disponibilidad
        disponibles = self.admin.buscar_paquetes(date(2025, 4, 1), date(2025, 6, 1))
        self.assertTrue(len(disponibles) >= 1)
        self.assertTrue(any(p.id_paquete == paquete.id_paquete for p in disponibles))

    def test_04_flujo_reservas(self):
        print("\nProbando flujo de reservas...")
        # Login como cliente
        cliente = self.auth.login(self.email_cliente, self.password)
        
        # Listar paquetes
        paquetes = self.admin.listar_paquetes()
        self.assertTrue(len(paquetes) > 0)
        paquete_id = paquetes[0].id_paquete
        
        # Crear reserva
        reserva = self.reservas.crear_reserva(cliente, paquete_id)
        self.assertIsNotNone(reserva.id_reserva)
        
        # Ver mis reservas
        mis_r = self.reservas.listar_mis_reservas(cliente)
        self.assertTrue(any(r.id_reserva == reserva.id_reserva for r in mis_r))

if __name__ == '__main__':
    unittest.main()
