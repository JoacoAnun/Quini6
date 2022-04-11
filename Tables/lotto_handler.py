# This file hanndles the data manipulation for the table Lottery_Historic
import itertools

import pandas as pd

from sql_conection import Session, engine, Base
from Tables.lotto import Lotto

Base.metadata.create_all(engine)


class LottoHandler:
    def __init__(self):
        self.session = Session()

    @staticmethod
    def add_record(data):
        columns = ['n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'date', 'lotto_id']
        df = pd.DataFrame(data, columns=columns)
        if not df.empty:
            df.to_sql(name=Lotto.__tablename__, con=engine, if_exists='append', index=False)

    def query_lottos_id(self):
        # Returns list of all lotto ids int database
        ids = self.session.query(Lotto.lotto_id).all()
        return list(itertools.chain(*ids))
