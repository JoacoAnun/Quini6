import platform
import itertools
import re

import sqlite3

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from Tables.lotto_handler import LottoHandler

WEBSITE = 'https://www.quini-6-resultados.com.ar/'


class WebDriver:

    def __init__(self):
        self.driver = None
        self.initialize_driver()

    def initialize_driver(self):
        PATH = '/usr/bin/google-chrome'
        if platform.system() == 'Darwin':
            PATH = '/Applications/Chromium.app/Contents/MacOS/Chromium'

        options = ChromeOptions()

        options.binary_location = PATH
        # Descomentar para no ver el navegador al correr el programa
        options.add_argument('headless')
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
        return self.driver

    def get_statistics(self):
        """
        Esta funcion devuelve una lista con
        Numero de loteria
        Cantidad de veces que salio el numero
        Ultima fecha en la que salio el numero
        """

        # Cargamos la pagina
        self.driver.get(WEBSITE)
        # Damos tiempo a que carge el pie de pagina
        WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.ID, 'footer')))

        # Buscamos el elemento estadistica (boton)
        estadisticas = self.driver.find_element(By.PARTIAL_LINK_TEXT, 'ESTADISTICAS').click()

        try:
            # Esperar 2 segundos para que la tabla esté correctamente cargada en el navegador
            WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, 'table')))

        # Si no se encuentra la tabla, cerramos el navegador
        except TimeoutException:
            print("Table not Found")
            self.driver.quit()

        # Creamos tabla vacia para recolectar los datos
        table = []
        # Calculamos el largo de la tabla
        table_lenght = len(self.driver.find_elements(By.XPATH, '//*[@class="table"]//tbody/tr'))

        # Iteramos sobre el largo de la tabla
        for i in range(1, table_lenght + 1):
            number = int(self.driver.find_element(By.XPATH, f'//*[@class="table"]//tbody/tr[{i}]/td[1]').text)
            frecuency = int(self.driver.find_element(By.XPATH, f'//*[@id="q_r1_barra_{str(i - 1)}"]').text)
            date = self.driver.find_element(By.XPATH, f'//*[@class="table"]//tbody/tr[{i}]/td[3]').text

            # Agregamos los datos a la tabla como tuplas
            table.append((number, frecuency, date))

        return table

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

        return tickets

    def get_lotteries(self):
        """
        Devuelve una lista con el historico de sorteos
        """
        # Cargamos la pagina
        self.driver.get(WEBSITE)
        # Damos tiempo a cargar la página
        self.driver.implicitly_wait(2)

        # Buscamos el elemento SORTEOS (boton)
        anteriores = self.driver.find_element(By.PARTIAL_LINK_TEXT, 'SORTEOS')
        anteriores.click()

        try:

            WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, 'row')))

        except:
            print('Table not found')

        # Listas de sorteos  (botones)
        len_sorteos = len(self.driver.find_elements(By.PARTIAL_LINK_TEXT, 'Sorteo'))

        winners = []

        lotto_ids = LottoHandler().query_lottos_id()

        # Buscamos cada ganador en cada sorteo
        for index in range(len_sorteos):
            lotto = int(self.driver.find_elements(By.PARTIAL_LINK_TEXT, 'Sorteo')[index].text.split()[1])

            # Si el sorteo se encuentra en base de datos, no hace falta cargar el valor nuevamente
            if lotto in lotto_ids:
                continue
            else:
                self.driver.find_elements(By.PARTIAL_LINK_TEXT, 'Sorteo')[index].click()

                # Extraemos el ganador del sorteo Tradicional
                winners.append(self._get_winner())

                self.driver.execute_script('window.history.go(-1)')
                self.driver.implicitly_wait(2)

        return winners

    def _get_winner(self):
        """
        Metodo privado para tomar los datos de los ganadores
        """

        try:
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'row')))

        except TimeoutException:
            print('No se encuentran los resultados del sorteo')

        table = self.driver.find_elements(By.CLASS_NAME, 'numeros')

        text = self.driver.find_element(By.XPATH, '//body/div[3]/h2').text
        lotto = re.search('[0-9]{4}', text)
        date = re.search('[0-9]+-[0-9]+-[0-9]+', text)
        # Deolvemos solamente el ganador del sorteo tradicional
        return table[0].text.replace(' ', '').split('-') + [date.group().replace('-', '/')] + [lotto.group()]

    def close(self):
        self.driver.quit()
