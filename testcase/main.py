import unittest
import platform
from locator import *

from modulos import WebDriver

WEBSITE = 'https://www.quini-6-resultados.com.ar/'


# Clase para comprobar la funcionalidad de modulos.py
class Quini6(unittest.TestCase, WebDriver):

    # Creamos el drivver
    def setUp(self):
   
        self.driver = self.initialize_driver()
        self.driver.get(WEBSITE)

    def test_title(self):
        assert 'Quini 6' in self.driver.title

    def test_sorteos_anteriores(self):
        self.driver.find_element(*MainPageSorteos.Quini_6_Sorteos).click()
        assert len(self.driver.find_elements(*TablaSorteosAnteriores.tabla)), 'Tabla no encontrada'

    def test_estadisticas(self):
        self.driver.find_element(*MainPageEstadisticas.Quini_6_Estadisticas).click()
        assert 'Estadísticas' in self.driver.title
        assert len(self.driver.find_elements(*TablaEstadisticas.estadisticas)), 'Tabla no encontrada'

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
