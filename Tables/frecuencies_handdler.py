# This file hanndles the data manipulation for the table Number_Frecuency_Historic
import itertools

import pandas as pd

from sql_conection import Session, engine, Base
from Tables.frecuencies import Frecuencies

Base.metadata.create_all(engine)


class FrecuenciesHandller:
    def __init__(self):
        self.session = Session()

    @staticmethod
    def add_record(data):
        df = pd.DataFrame(data, columns=['number', 'frecuency', 'date'])
        df.to_sql(name=Frecuencies.__tablename__, con=engine, if_exists='replace', index=False)

    def query_frequent_numbers(self):
        # Returns the list of freqcuent numbers with its frecuency
        frecuencies = self.session.query(Frecuencies.frecuency).all()
        frecuencies = list(itertools.chain(*frecuencies))
        numbers = self.session.query(Frecuencies.number).all()
        numbers = list(itertools.chain(*numbers))
        return numbers, frecuencies
