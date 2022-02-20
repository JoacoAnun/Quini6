from Tables.frecuencies_handdler import FrecuenciesHandller
from Tables.lotto_handler import LottoHandler

from modulos import *

my_chrome = WebDriver()


def udpate_frecuency_table():
    frecuencies = my_chrome.get_statistics()
    FrecuenciesHandller().add_record(data=frecuencies)


LottoHandler()
udpate_frecuency_table()
