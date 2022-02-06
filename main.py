import random
import numpy as np
from numpy.random import Generator

import math
import locale
from random import choice
from modulos import *
import ddbb
import sqlite3

factorial_46 = math.factorial(46)


def format_number(number):
    """
    Asumimos que recibe un numero
    Devuelve en formato string de la moneda local
    """
    if platform.system() == 'Darwin':
        return number

    locale.setlocale(locale.LC_ALL, 'es_AR.UTF-8')
    return locale.currency(number, grouping=True, international=True)


def get_delta_numbers():
    np.random.seed()
    lista_delta = []
    # Parte 1 del sistema delta
    n_1 = np.random.randint(0, 6)
    n_2 = np.random.randint(1, 8, 2)
    n_3 = np.random.randint(7, 10, 1)
    n_4 = np.random.randint(8, 16, 2)

    lista_delta.extend([n_1, *n_2, *n_3, *n_4])

    # Repetir hasta que la suma sea menor a 46
    if sum(lista_delta) > 45:
        return get_delta_numbers()
    else:
        random.shuffle(lista_delta)
        return lista_delta


def delta_system():
    """
    Funcion que elije y devuelve los numeros a jugar de la loteria basados en el sistema delta
    """

    lottery_ticket_play = []

    numbers = get_delta_numbers()
    # Primer numero a jugar es el primer numero de numbers
    lottery_ticket_play.append(numbers[0])
    # El resto de los numeros se generan
    # sumando el siguiente número delta al número de lotteria seleccionado en el paso anterior
    for i in range(1, len(numbers)):
        lottery_ticket_play.append(lottery_ticket_play[i - 1] + numbers[i])

    # Control de numeros duplicados en el ticket de loteria
    lottery_ticket_play = set(lottery_ticket_play)
    while len(lottery_ticket_play) < 6:
        # Reemplazamos el número faltante por uno de los 6 numeros más frecuentes que no se encuentre ya en juego
        frecuent = get_frecuent_numbers(most=True)
        lottery_ticket_play.add(choice([j for j in frecuent if j not in list(lottery_ticket_play)]))

    return sorted(list(lottery_ticket_play))


def lotter_plays(n=1):
    """
    Devuelve los numeros y cantidad de tickets que se deseen jugar
    """
    tickets = []
    for _ in range(n):
        tickets.append(delta_system())

    return tickets


def cost_benefit(tickets=1):
    """
    Recibe la cantidad de tickets a jugar
    Imprime la relacion costo beneficio de jugar al quini
    """

    # Falta ver como poder calcular el pozo del proximo sorteo
    # Actualmente devuelve el costo beneficio del último sorteo realizado

    chrome_driver = WebDriver()

    aciertos = 6
    # Obtenemos el valor de los tres tickets a jugar al tradicional
    cost = np.array(chrome_driver.get_ticket_cost()[0])

    win_cost = tickets * cost

    # Obtenemos los pozos de premios de la tradicional y segunda
    jackpots = np.array(chrome_driver.get_jackpot_values())

    beneficio = jackpots - win_cost

    for i in range(3):
        print(f'Relacion costo - beneficio comprando {tickets} ticket/s '
              f'con {aciertos} aciertos: ${format_number(beneficio[i])}')
        aciertos -= 1

    print(f"""
Comprando {tickets} ticket/s:
Probabilidad de ganar con 6 aciertos: {1 * tickets / (factorial_46 / (math.factorial(6) * math.factorial(40))):.10f}
Probabilidad de ganar con 5 aciertos: {1 * tickets / (factorial_46 / (math.factorial(5) * math.factorial(41))):.10f}
Probabilidad de ganar con 4 aciertos: {1 * tickets / (factorial_46 / (math.factorial(4) * math.factorial(42))):.10f}
        """)
    chrome_driver.close()


def get_frecuent_numbers(most=True):
    """
    Devuelve los 6 numeros más frecuentes de la loteria de la base de datos en una lista si most es True
    Caso contrario si es False
    """

    if most:
        order = 'DESC'
    else:
        order = 'ASC'

    conection = sqlite3.connect('base_de_datos.db')
    cursor = conection.cursor()

    cursor.execute(f"SELECT * FROM FRECUENCIAS_HISTORICAS ORDER BY FRECUENCIA {order}")
    rows = cursor.fetchall()[:6]

    conection.close()

    frecuents = []
    for row in rows:
        frecuents.append(row[0])

    return sorted(frecuents)


def lottery_simulator():
    """
    Simula un juego de loteria y devuelve el número ganador en forma de lista
    """
    np.random.seed()
    lotto_number = sorted(np.random.choice(46, size=6, replace=False))

    return lotto_number


def is_winner(plays):
    """
    Imprime el ticket ganador con la cantidad de aciertos
    """

    tickets = lotter_plays(plays)
    lotto_winner = lottery_simulator()
    winner_tickets = []
    for ticket in tickets:
        hits = sum(np.equal(ticket, lotto_winner))
        if hits >= 4:
            winner_tickets.extend([ticket, hits])

    if winner_tickets:
        print(f'Ticket/s ganador/es:')
        print(winner_tickets)

    else:
        print('No hay ticket ganador')

    print(f'Numero ganador: {lotto_winner}')


if __name__ == '__main__':
    # Decomentar para actualizar la base de datos con todos los sorteos
    ddbb.full_ddbb_update()

    # jugadas = 10000
    # # Simula la compra de n tickets y un numero ganador de loteria.
    # is_winner(jugadas)
    # cost_benefit(jugadas)
