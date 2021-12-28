import platform

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re


WEBSITE = 'https://www.quini-6-resultados.com.ar/'

# JERE: Esto lo hice para que si el sistema operativo es Mac, busque el webdriver en Applications


class WebDriver(object):

    def __init__(self):
        self.driver = None
        self.generate_browser()

    def generate_browser(self):

        if platform.system() == 'Linux':
            PATH = '/usr/bin/chromedriver'
        elif platform.system() == 'Darwin':
            PATH = '/Applications/Chromium.app/Contents/MacOS/Chromium'

        options = ChromeOptions()

        # JOACO, tuve que cambiar la direccion al ejecutable porque con el chromedriver me da error
        # Habria que agregar un if o algo similar a lo anterior para caso MAC
        options.binary_location = '/usr/bin/google-chrome'

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
        self.driver = webdriver.Chrome(PATH, chrome_options=options)

    def get_statistics(self):
        """
        Esta funcion devuelve una lista con
        Numero de loteria
        Cantidad de veces que salio el numero
        Ultima fecha en la que salio el numero
        """

        # Cargamos la pagina
        self.driver.get(WEBSITE)
        # Damos tiempo a cargar la página
        self.driver.implicitly_wait(2)

        # Buscamos el elemento estadistica (boton)
        estadisticas = self.driver.find_element(By.PARTIAL_LINK_TEXT, 'ESTADISTICAS')

        # Cargamos la accion al driver, y ejecutamos con perform
        accion = ActionChains(self.driver)
        accion.click(estadisticas)
        accion.perform()

        try:
            # Esperar 5 segundos para que la tabla esté correctamente cargada en el navegador
            WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, 'table')))

        # Si no se encuentra la tabla, cerramos el navegador
        except:
            print("Tabla no encontrada")
            self.driver.quit()

        # Creamos tabla vacia para recolectar los datos
        tabla = []
        # Calculamos el largo de la tabla
        largo_tabla = len(self.driver.find_elements(By.XPATH, '//*[@class="table"]//tbody/tr'))

        # Iteramos sobre el largo de la tabla
        for i in range(1, largo_tabla + 1):
            numero = self.driver.find_element(By.XPATH, f'//*[@class="table"]//tbody/tr[{i}]/td[1]').text
            frecuencia = int(self.driver.find_element(By.XPATH, f'//*[@id="q_r1_barra_{str(i - 1)}"]').text)
            fecha = self.driver.find_element(By.XPATH, f'//*[@class="table"]//tbody/tr[{i}]/td[3]').text

            # Agregamos los datos a la tabla como tuplas
            tabla.append((numero, frecuencia, fecha))

        return tabla

    def get_jackpot_values(self):
        """
        Devuelve una lista con los premios de los ganadores en el Quini Tradicional
        a 6 aciertos, a 5 aciertos y a 4 aciertos respectivamente, como floats
        """

        self.driver.get(WEBSITE)
        # Damos tiempo a cargar la página
        self.driver.implicitly_wait(2)

        jackpots = []

        for i in range(2, 5):
            jackpots.append(float(
                self.driver.find_element(By.XPATH, f'//*[@class="table"]//tbody/tr[{i}]/td[3]').text.lstrip('$ ')
                    .replace('.', '').replace(',', '.')))

        self.driver.quit()
        return jackpots

    def get_ticket_cost(self):
        """
        Devuelve el costo de los tickets, como ints
        """
        # Cargamos la pagina
        self.driver.get(WEBSITE)
        # Damos tiempo a cargar la página
        self.driver.implicitly_wait(2)

        tickets = []
        for i in range(1, 4):
            tickets.append(
                int((self.driver.
                     find_element(By.XPATH, f'//*[@class="panel-body"]//ul/li[{i}]/p/b').text.replace('$', ''))))

        self.driver.quit()
        return tickets

    def get_sortes_anteriores(self):
        """
        Devuelve una lista con el historico de sorteos a un archivo txt
        """
        # Cargamos la pagina
        self.driver.get(WEBSITE)
        # Damos tiempo a cargar la página
        self.driver.implicitly_wait(2)

        # Buscamos el elemento SORTEOS (boton
        anteriores = self.driver.find_element(By.PARTIAL_LINK_TEXT, 'SORTEOS')

        # Navegamos a la página de Sorteos anteriores
        action = ActionChains(self.driver)
        action.click(anteriores)
        action.perform()

        try:

            WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, 'row')))

        except:
            print('No se encuentra la tabla de sorteos previos')

        # Listas de sorteos  (botones)
        len_sorteos = len(self.driver.find_elements(By.PARTIAL_LINK_TEXT, 'Sorteo'))

        ganadores = []

        # Buscamos cada ganador en cada sorteo
        for index in range(len_sorteos):
            self.driver.find_elements(By.PARTIAL_LINK_TEXT, 'Sorteo')[index].click()
            action.perform()
            self.driver.implicitly_wait(2)

            # Extraemos el ganador del sorteo Tradicional
            ganadores.append(self.__get_winner())

            self.driver.execute_script('window.history.go(-1)')
            self.driver.implicitly_wait(2)

        self.driver.quit()
        return ganadores

    def __get_winner(self):
        """
        Metodo privado para tomar los datos de los ganadores
        """
        # JOACO lo defini privado, ya que si lo llamo por fuera de la clase
        # dara error al no cargar ninguna página (es traida de la funcion get_sorteos_anteriores)
        try:
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'row')))

        except:
            print('No se encuentran los resultados del sorteo')

        tabla = self.driver.find_elements(By.CLASS_NAME, 'numeros')

        texto = self.driver.find_element(By.XPATH, '//body/div[3]/h2').text
        sorteo = re.search('[0-9]{4}', texto)
        fecha = re.search('[0-9]+-[0-9]+-[0-9]+', texto)
        # Deolvemos solamente el ganador del sorteo tradicional
        return tabla[0].text.replace(' ', '').split('-') + [fecha.group().replace('-', '/')] + [sorteo.group()]

    def get_last_lottery(self):
        """
        Devielve fecha y numero del ultimo sorteo
        """

        self.driver.get(WEBSITE)
        # Damos tiempo a cargar la página
        self.driver.implicitly_wait(2)

        texto = self.driver.find_element(By.CLASS_NAME, 'lead').text
        sorteo = int(re.search('[0-9]{4}$', texto).group())
        fecha = re.search('[0-9]{2}/[0-9]{2}/[0-9]{4}', texto).group()
        ganador = self.driver.find_element(By.XPATH, '//*[@id="q_pnlResultados"]/table/tbody/tr[2]/td').text
        ganador = list(map(int, ganador.replace(' ', '').split('-')))

        self.driver.quit()
        return ganador + [fecha] + [sorteo]


my_chrome = WebDriver()