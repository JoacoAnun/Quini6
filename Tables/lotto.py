# Lotto Table creation

from sql_conection import Base
from sqlalchemy import Column, Integer, DateTime


class Lotto(Base):
    __tablename__ = 'Lottery_Historic'

    n1 = Column(Integer)
    n2 = Column(Integer)
    n3 = Column(Integer)
    n4 = Column(Integer)
    n5 = Column(Integer)
    n6 = Column(Integer)
    date = Column(DateTime)
    lotto_id = Column(Integer, primary_key=True)
