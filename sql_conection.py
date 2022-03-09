from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from decouple import config

SYSTEM = config('SYSTEM')
DATABASE = config('DATABASE')
PORT = config('PORT')
USER = config('USER')
PASSWORD = config('PASSWORD')
HOST = config('HOST')

engine = create_engine(f'{SYSTEM}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}')
Session = sessionmaker(bind=engine)
Base = declarative_base()


