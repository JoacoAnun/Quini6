from locator import *
from selenium.webdriver.support.ui import WebDriverWait


# Clase de pagina base
class BasePage(object):
    def __init__(self, driver):
        self.driver = driver


# Clase para controlar la pagina principal y el acceso a distintas partes de la pagina
class MainPage(BasePage):
    def is_title_matches(self):
        return 'Quini 6' in self.driver.title

    # Acceso a pagina de todos los Sorteos
    def click_Quini6_Sorteos(self):
        element = self.driver.find_element(*MainPageSorteos.Quini_6_Sorteos)
        element.click()

    # Acceso a la pagina de las estadisitcas historicas
    def click_Quini6_Estadisticas(self):
        element = self.driver.find_element(*MainPageEstadisticas.Quini_6_Estadisticas)
        element.click()


# Clase para el manejo de los elementos la pagina de Sorteos Anteriores
class SorteosAnteriores(BasePage):
    def table_exists(self):
        largo_tabla = len(self.driver.find_elements(*TablaSorteosAnteriores.tabla))
        return largo_tabla


# Clase para el manejo de los elementos la pagina de Sorteos Anteriores
class Quini6Estadisticas(BasePage):
    def is_title_match(self):
        return 'Estadísticas' in self.driver.title

    def tabla_sorteos_anteriores(self):
        # Devuelve True si la tabla fue existe, False caso contratio
        return bool(WebDriverWait(self.driver, 2).
                    until(lambda driver: driver.find_element(*TablaEstadisticas.estadisticas)))






