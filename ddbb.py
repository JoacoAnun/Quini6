# Base de Datos
import sqlite3
from modulos import *


def data_base_creation():
    """
    Crea la base de datos, si esta no existe
    """
    con = sqlite3.connect('base_de_datos.db')
    cursor = con.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS FRECUENCIAS_HISTORICAS (NUMERO INTEGER, FRECUENCIA INTEGER,'
                   'FECHA VARCHAR(50))')

    cursor.execute('CREATE TABLE IF NOT EXISTS SORTEOS (SORTEO INTEGER,'
                   'N1 INTEGER, N2 INTEGER, N3 INTEGER, N4 INTEGER, N5 INTEGER, N6 INTEGER,'
                   'FECHA VARCHAR(20), NRO_SORTEO INT PRIMARY KEY)')

    con.close()


def update_ddbb():
    """
    Carga solamente el último sorteo a la base de datos
    """
    my_chrome = WebDriver()
    ganadores = my_chrome.get_last_lottery()

    conection = sqlite3.connect('base_de_datos.db')
    cursor = conection.cursor()

    print('Actualizando base de datos')
    cursor.execute('INSERT OR REPLACE INTO SORTEOS VALUES (?,?,?,?,?,?,?,?)', ganadores)
    conection.commit()

    conection.close()
    my_chrome.close()
    return


# Funcion para actualizar la base de datos con los ultimos sorteos mostrados en la página
def full_ddbb_update():
    chrome_driver = WebDriver()
    conexion = sqlite3.connect('base_de_datos.db')
    cursor = conexion.cursor()
    ganadores_anteriores = chrome_driver.get_sorteos_anteriores()
    print('Actualizando base de datos')
    for ganador in ganadores_anteriores:
        cursor.execute('INSERT OR REPLACE INTO SORTEOS VALUES (?,?,?,?,?,?,?,?)', ganador)
        conexion.commit()

    conexion.close()
    chrome_driver.close()


def update_number_frecuency():
    chrome_driver = WebDriver()
    con = sqlite3.connect('base_de_datos.db')
    cur = con.cursor()

    tabla_frecuencias = chrome_driver.get_statistics()
    print(tabla_frecuencias)
    for entrada in tabla_frecuencias:
        cur.execute('INSERT OR REPLACE INTO FRECUENCIAS_HISTORICAS VALUES (?,?,?)', entrada)
        con.commit()

    chrome_driver.close()
    con.close()
