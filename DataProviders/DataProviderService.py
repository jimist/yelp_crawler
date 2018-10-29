from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import datetime
import hashlib
import time

from Models import init_database

class DataProviderService:
	session = None
	engine = None
	DBEngine = None

	@staticmethod
	def init_database():
		init_database(DataProviderService.engine)

	@staticmethod
	def startSession():
		#engine = import database uri from config.py
		DataProviderService.engine = engine
		DataProviderService.DBEngine = create_engine(engine)
		db_session = sessionmaker(bind=DataProviderService.DBEngine)
		DataProviderService.session = db_session()
		return DataProviderService.session

	@staticmethod
	def getSession():
		if DataProviderService.session is not None:
			return DataProviderService.session
		else:
			return DataProviderService.startSession()

