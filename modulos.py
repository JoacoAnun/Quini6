# Modulos has the class and functions to navigate through https://www.quini-6-resultados.com.ar/,
# scrapping the needed infromation

import platform
import re

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
        # Linux standar chrome path location
        PATH = '/usr/bin/google-chrome'
        if platform.system() == 'Darwin':
            # For macOS users
            PATH = '/Applications/Chromium.app/Contents/MacOS/Chromium'

        options = ChromeOptions()
        options.binary_location = PATH

        # Uncomment to hide website while the program is running
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
        Returns all numbers and its frequency of appearance

        Returns:
            list: list of tuples of all numbers and its frequency of appearance
        """

        # Load website
        self.driver.get(WEBSITE)
        # 2 seconds to let the webpage load 100%
        WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.ID, 'footer')))

        # Look up for button ESTADISTICAS and click it
        self.driver.find_element(By.PARTIAL_LINK_TEXT, 'ESTADISTICAS').click()

        try:
            # 2 seconds wating until the table is fully loaded
            WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, 'table')))

        # If table not found raise error
        except TimeoutException:
            print("Table not Found")
            self.driver.quit()

        # empty table to store data
        table = []

        table_lenght = len(self.driver.find_elements(By.XPATH, '//*[@class="table"]//tbody/tr'))

        # Iteramos sobre el largo de la tabla
        for i in range(1, table_lenght + 1):
            number = int(self.driver.find_element(By.XPATH, f'//*[@class="table"]//tbody/tr[{i}]/td[1]').text)
            frecuency = int(self.driver.find_element(By.XPATH, f'//*[@id="q_r1_barra_{str(i - 1)}"]').text)
            date = self.driver.find_element(By.XPATH, f'//*[@class="table"]//tbody/tr[{i}]/td[3]').text

            table.append((number, frecuency, date))

        return table

    def get_jackpot_values(self):
        """
        Returns lottery jackpot

        Returs:
            float: lottery jackpot
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
        Returns tieckt costs for playing the lottery

        Returs:
            list: list of integer value for ticket costs
        """

        self.driver.get(WEBSITE)
        self.driver.implicitly_wait(2)

        ticket_costs = []
        for i in range(1, 4):
            ticket_costs.append(
                int((self.driver.
                     find_element(By.XPATH, f'//*[@class="panel-body"]//ul/li[{i}]/p/b').text.replace('$', ''))))

        return ticket_costs

    def get_lotteries(self):
        """
        Returns all avaliable lottery results

        Returs:
            list: past lottery winners available
        """

        self.driver.get(WEBSITE)
        self.driver.implicitly_wait(2)

        self.driver.find_element(By.PARTIAL_LINK_TEXT, 'SORTEOS').click()

        try:

            WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, 'row')))

        except TimeoutException:
            print('Table not found')

        # Listas de sorteos  (botones)
        len_lottos_table = len(self.driver.find_elements(By.PARTIAL_LINK_TEXT, 'Sorteo'))

        winners = []

        # Queries already saved lottery results
        lotto_ids = LottoHandler().query_lottos_id()

        for index in range(len_lottos_table):
            lotto = int(self.driver.find_elements(By.PARTIAL_LINK_TEXT, 'Sorteo')[index].text.split()[1])

            # If lotto not in database, load winner
            if lotto not in lotto_ids:

                self.driver.find_elements(By.PARTIAL_LINK_TEXT, 'Sorteo')[index].click()
                # Extraemos el ganador del sorteo Tradicional
                winners.append(self._get_winner())

                self.driver.execute_script('window.history.go(-1)')
                self.driver.implicitly_wait(2)

            else:
                continue

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
