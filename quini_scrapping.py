import numpy as np
import math
import locale

from modulos import *

factorial_46 = math.factorial(46)


def format_number(number):
    """
    Asumimos que recibe un numero
    Devuelve en formato string de la moneda local
    """
    # JERE: Esto lo hice simplemente porque Mac tiene problemas con los locale. De todas formas esta muy bueno destacar este if
    # Fijate que te deja ver muy limpiamente el comportamiento del metodo. Si es MacOS, devuelve number y punto. Si no es MacOS
    # seguis leyendo y ves que hace. Esto se llama fail-fast. No siempre se puede hacer, pero cuando se puede es mucho mas limpio
    # Mientras vayamos avanzando vamos a encontrar seguramente algun otro ejemplo para aplicarlo y que quede mucho mas explicito el comportamiento
    if platform.system() == 'Darwin':
        return number

    locale.setlocale(locale.LC_ALL, 'es_AR.UTF-8')
    return locale.currency(number, grouping=True, international=True)


def cost_benefit(tickets=1):
    """
    Recibe la cantidad de tickets a jugar
    Imprime la relacion costo beneficio de jugar al quini
    """

    # Falta ver como poder calcular el pozo del proximo sorteo
    # Actualmente devuelve el costo beneficio del ultimo sorteo realizado

    aciertos = 6
    # Obtenemos el valor de los tres tickets a jugar al tradicional
    cost = get_ticket_cost()[0]

    win_cost = tickets * cost

    # Obtenemos los pozos de premios de la tradicional y segunda
    jackpots = np.array(get_jackpot_values())

    beneficio = jackpots - win_cost

    for i in range(3):
        print(f'Relacion costo - beneficio comprando {tickets} ticket/s '
              f'con {aciertos} aciertos: ${format_number(beneficio[i])}')
        aciertos -= 1

    print(f"""
        Comprando {tickets} ticket/s:
        Probabilidad de ganar con 6 aciertos: {1*tickets / (factorial_46 / (math.factorial(6) * math.factorial(40))):.10f}
        Probabilidad de ganar con 5 aciertos: {1*tickets / (factorial_46 / (math.factorial(5) * math.factorial(41))):.10f}
        Probabilidad de ganar con 4 aciertos: {1*tickets / (factorial_46 / (math.factorial(4) * math.factorial(42))):.10f}
        """)


# FIXME: Se podría simplificar este metodo quini_scrapping con el main y llamar a "cost_benefit" directamente en el main
def quini_scrapping():
    cost_benefit(100)


if __name__ == '__main__':
    quini_scrapping()
