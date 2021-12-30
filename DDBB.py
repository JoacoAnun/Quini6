# Base de Datos
import sqlite3
from modulos import *


def update_DDBB():
    my_chrome = WebDriver()
    ganadores = my_chrome.get_last_lottery()

    conexion = sqlite3.connect('Base de Datos Sorteo.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM SORTEOS')

    ultimo_registro = cursor.fetchall()[-1]
    largo_tabla, ultimo_sorteo = ultimo_registro[0], ultimo_registro[-1]

    actualizar = ganadores[-1] != ultimo_sorteo

    if actualizar:
        print('Actualizando base de datos')
        ganadores.insert(0, largo_tabla + 1)
        cursor.execute('INSERT OR REPLACE INTO SORTEOS VALUES (?,?,?,?,?,?,?,?,?)', ganadores)
        conexion.commit()

        print('Base de datos actualizada')
    else:
        print('Base de datos no necesita actualizarse')

    conexion.close()
    my_chrome.quit_browser()
    return


# Descomentar para crear la base de datos si no existe
# cursor.execute('CREATE TABLE IF NOT EXISTS SORTEOS (SORTEO INTEGER,'
#               'N1 INTEGER, N2 INTEGER, N3 INTEGER, N4 INTEGER, N5 INTEGER, N6 INTEGER,'
#               'FECHA VARCHAR(20), NRO_SORTEO INT PRIMARY KEY)')

update_DDBB()
