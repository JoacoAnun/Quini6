from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re

PATH = '/usr/bin/chromedriver'
WEBSITE = 'https://www.quini-6-resultados.com.ar/'


def go_webpage(path, website):
    """
    Carga la pagina a explorar
    """
    driver = webdriver.Chrome(path)
    driver.get(website)
    # Damos tiempo a cargar la pagina
    driver.implicitly_wait(2)
    return driver


def get_statistics():
    """
    Esta funcion devuelve una lista con
    Numero de loteria
    Cantidad de veces que salio el numero
    Ultima fecha en la que salio el numero
    """
    # Cargamos la pagina
    driver = go_webpage(PATH, WEBSITE)

    # Buscamos el elemento estadistica (boton)
    estadisticas = driver.find_element(By.PARTIAL_LINK_TEXT, 'ESTADISTICAS')

    # Cargamos la accion al driver, y ejecutamos con perform
    accion = ActionChains(driver)
    accion.click(estadisticas)
    accion.perform()

    try:
        # Esperar 5 segundos para que la tabla este correctamente cargada en el navegador
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, 'table')))

    # Si no se encuentra la tabla, cerramos el navegador
    except:
        print("Tabla no encontrada")
        driver.quit()

    # Creamos tabla vacia para recolectar los datos
    tabla = []
    # Calculamos el largo de la tabla
    largo_tabla = len(driver.find_elements(By.XPATH, '//*[@class="table"]//tbody/tr'))

    # Iteramos sobre el largo de la tabla
    for i in range(1, largo_tabla + 1):
        numero = driver.find_element(By.XPATH, f'//*[@class="table"]//tbody/tr[{i}]/td[1]').text
        frecuencia = int(driver.find_element(By.XPATH, f'//*[@id="q_r1_barra_{str(i - 1)}"]').text)
        fecha = driver.find_element(By.XPATH, f'//*[@class="table"]//tbody/tr[{i}]/td[3]').text

        # Agregamos los datos a la tabla como tuplas
        tabla.append((numero, frecuencia, fecha))

    return tabla


def get_jackpot_values():
    """
    Devuelve una lista con los premios de los ganadores en el Quini Tradicional
    a 6 aciertos, a 5 aciertos y a 4 aciertos respectivamente, como floats
    """

    driver = go_webpage(PATH, WEBSITE)

    jackpots = []

    for i in range(2, 5):
        jackpots.append(float(
            driver.find_element(By.XPATH, f'//*[@class="table"]//tbody/tr[{i}]/td[3]').text.lstrip('$ ')
                .replace('.', '').replace(',', '.')))

    return jackpots


def get_ticket_cost():
    """
    Devuelve el costo de los tickets, como ints
    """
    # Cargamos la pagina
    driver = go_webpage(PATH, WEBSITE)

    tickets = []
    for i in range(1, 4):
        tickets.append(
            int((driver.find_element(By.XPATH, f'//*[@class="panel-body"]//ul/li[{i}]/p/b').text.replace('$', ''))))
    return tickets


def get_sortes_anteriores():
    """
    Devuelve una lista con el historico de sorteos a un archivo txt
    """
    # Cargamos la pagina
    driver = go_webpage(PATH, WEBSITE)

    # Buscamos el elemento SORTEOS (boton
    anteriores = driver.find_element(By.PARTIAL_LINK_TEXT, 'SORTEOS')

    # Navegamos a la pagina de Sorteos anteriores
    action = ActionChains(driver)
    action.click(anteriores)
    action.perform()

    try:

        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, 'row')))

    except:
        print('No se encuentra la tabla de sorteos previos')

    # Listas de sorteos  (botones)
    len_sorteos = len(driver.find_elements(By.PARTIAL_LINK_TEXT, 'Sorteo'))

    ganadores = []

    # Buscamos cada ganador en cada sorteo
    for index in range(len_sorteos):
        driver.find_elements(By.PARTIAL_LINK_TEXT, 'Sorteo')[index].click()
        action.perform()
        driver.implicitly_wait(2)

        # Extraemos el ganador del sorteo Tradicional
        ganadores.append(get_winner(driver))

        driver.execute_script('window.history.go(-1)')
        driver.implicitly_wait(2)

    driver.quit()
    return ganadores


def get_winner(driver):
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'row')))

    except:
        print('No se encuentran los resultados del sorteo')

    tabla = driver.find_elements(By.CLASS_NAME, 'numeros')

    texto = driver.find_element(By.XPATH, '//body/div[3]/h2').text
    sorteo = re.search('[0-9]{4}', texto)
    fecha = re.search('[0-9]+-[0-9]+-[0-9]+', texto)
    # Deolvemos solamente el ganador del sorteo tradicional
    return tabla[0].text.replace(' ', '').split('-') + [fecha.group().replace('-', '/')] + [sorteo.group()]


def get_last_lottery():
    """
    Devielve fecha y numero del ultimo sorteo
    """
    driver = go_webpage(PATH, WEBSITE)

    texto = driver.find_element(By.CLASS_NAME, 'lead').text
    sorteo = int(re.search('[0-9]{4}$', texto).group())
    fecha = re.search('[0-9]{2}/[0-9]{2}/[0-9]{4}', texto).group()
    ganador = driver.find_element(By.XPATH, '//*[@id="q_pnlResultados"]/table/tbody/tr[2]/td').text
    ganador = list(map(int, ganador.replace(' ', '').split('-')))
    return ganador + [fecha] + [sorteo]




