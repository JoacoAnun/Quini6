from Tables.frecuencies_handdler import FrecuenciesHandller
from Tables.lotto_handler import LottoHandler

from modulos import *

my_chrome = WebDriver()


def update_frecuency_table():
    frecuencies = my_chrome.get_statistics()
    FrecuenciesHandller().add_record(data=frecuencies)


def update_lotto_table():
    lottos_to_update = my_chrome.get_lotteries()
    LottoHandler().add_record(lottos_to_update)


# Uncomment to update database
# update_lotto_table()
# update_frecuency_table()
