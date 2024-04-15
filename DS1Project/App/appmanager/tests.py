# tests/test_models.py
from django.test import TestCase
from appmanager.models import VehiculoVenta 

class VehiculoVentaTest(TestCase):
    def test_crear_vehiculo_venta(self):
        
        vehiculo = VehiculoVenta.objects.create(
            vehvnt_placa='ABC123',
            vehvnt_marca='Toyota',
            vehvnt_modelo='Corolla',
            vehvnt_color='Rojo',
            vehvnt_anio='2022',
            vehvnt_precioneto=15000.00,
            vehvnt_disponible=True,
            vehvnt_vigente=True
        )
        
       
        self.assertEqual(vehiculo.vehvnt_placa, 'ABC123')
        self.assertEqual(vehiculo.vehvnt_marca, 'Toyota')
        self.assertEqual(vehiculo.vehvnt_modelo, 'Corolla')
        self.assertEqual(vehiculo.vehvnt_color, 'Rojo')
        self.assertEqual(vehiculo.vehvnt_anio, '2022')
        self.assertEqual(vehiculo.vehvnt_precioneto, 15000.00)
        self.assertTrue(vehiculo.vehvnt_disponible)
        self.assertTrue(vehiculo.vehvnt_vigente)

       
        self.assertIsNotNone(vehiculo.pk)
