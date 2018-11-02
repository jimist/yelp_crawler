from config import DATABASE_URI as engine

from Models import init_database

init_database(engine)

