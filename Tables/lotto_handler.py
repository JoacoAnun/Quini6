# This file hanndles the data manipulation for the table Lottery_Historic

from sql_conection import Session, engine, Base
from Tables.lotto import Lotto

Base.metadata.create_all(engine)


class LottoHandler:
    def __init__(self):
        self.session = Session()

    def add_record(self):
        pass
