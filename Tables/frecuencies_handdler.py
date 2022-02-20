# This file hanndles the data manipulation for the table Number_Frecuency_Historic

from sql_conection import Session, engine, Base
from Tables.frecuencies import Frecuencies

Base.metadata.create_all(engine)


class FrecuenciasHandller:
    def __init__(self):
        self.session = Session()

    def add_record(self):
        pass
