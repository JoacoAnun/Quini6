from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from decouple import config

engine = create_engine(config('DATABASE_URL'))
Session = sessionmaker(bind=engine)
Base = declarative_base()


