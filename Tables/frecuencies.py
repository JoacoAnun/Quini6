# Frecuencies Table creation

from sql_conection import Base
from sqlalchemy import Column, Integer, DateTime


class Frecuencies(Base):
    __tablename__ = 'Number_Frecuency_Historic'
    number = Column(Integer, primary_key=True)
    frecuency = Column(Integer)
    date = Column(DateTime)
