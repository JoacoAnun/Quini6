import unittest
import platform

from selenium import webdriver
from selenium.webdriver import ChromeOptions

import page

WEBSITE = 'https://www.quini-6-resultados.com.ar/'


# Clase para comprobar la funcionalidad de modulos.py
class Quini6(unittest.TestCase):

    # Creamos el drivver
    def setUp(self):
        if platform.system() == 'Linux':
            PATH = '/usr/bin/google-chrome'
        else:
            PATH = '/Applications/Chromium.app/Contents/MacOS/Chromium'

        options = ChromeOptions()

        options.binary_location = PATH
        # Descomentar para no ver el navegador al correr el programa
        # options.add_argument('headless')
        options.add_argument('hide-scrollbars')
        options.add_argument('disable-gpu')
        options.add_argument('no-sandbox')
        options.add_argument('data-path=/tmp/chromium/data-path')
        options.add_argument('disk-cache-dir=/tmp/chromium/cache-dir')
        options.add_argument('disable-infobars')
        # Disable web security for get ember components via execute-scripts
        options.add_argument('disable-web-security')
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.maximize_window()
        self.driver.get(WEBSITE)

    def test_title(self):
        mainPage = page.MainPage(self.driver)
        assert mainPage.is_title_matches()

    def test_sorteos_anteriores(self):
        mainPage = page.MainPage(self.driver)
        mainPage.click_Quini6_Sorteos()
        sortespage = page.SorteosAnteriores(self.driver)
        tabla = sortespage.table_exists()
        assert tabla > 0

    def test_estadisticas(self):
        mainPage = page.MainPage(self.driver)
        mainPage.click_Quini6_Estadisticas()
        estadisticas = page.Quini6Estadisticas(self.driver)
        assert estadisticas.is_title_match()
        is_table = estadisticas.tabla_sorteos_anteriores()
        assert is_table

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
