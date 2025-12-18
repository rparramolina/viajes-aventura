import unittest
from datetime import date
from servicios.autenticacion import ServicioAutenticacion
from modelos.paquete import PaqueteTuristico
from modelos.destino import Destino

class TestViajesAventura(unittest.TestCase):
    
    def test_modelo_paquete_duracion(self):
        p = PaqueteTuristico(1, "Test", date(2023, 1, 1), date(2023, 1, 5))
        self.assertEqual(p.duracion_dias, 4)

    def test_calculo_precio_paquete(self):
        p = PaqueteTuristico(1, "Test", date(2023, 1, 1), date(2023, 1, 5))
        d1 = Destino(1, "D1", "Desc", "Act", 100.0)
        d2 = Destino(2, "D2", "Desc", "Act", 200.0)
        p.agregar_destino(d1)
        p.agregar_destino(d2)
        # La lógica de suma está en el repo o manual, aquí probamos si la propiedad se maneja bien
        precio_calculado = sum(d.costo_base for d in p.destinos)
        self.assertEqual(precio_calculado, 300.0)


if __name__ == '__main__':
    unittest.main()
