from selenium.webdriver.common.by import By


class MainPageSorteos(object):
    # Titulo de la pagina principal
    Quini_6_Sorteos = (By.XPATH, '/html/body/div[1]/div/ul/li[3]/a')


class MainPageEstadisticas(object):
    # Ubicacion del boton para obtener las estadisticas de los sorteos
    Quini_6_Estadisticas = (By.XPATH, '/html/body/div[1]/div/ul/li[2]/a')


class TablaSorteosAnteriores(object):
    # Ubicacion de todos los botones de los sorteos anteriores
    tabla = (By.PARTIAL_LINK_TEXT, 'Sorteo')


class TablaEstadisticas(object):
    # Ubicacion de la tabla de estadisticas
    estadisticas = (By.XPATH, '//*[@class="table"]//tbody/tr')
