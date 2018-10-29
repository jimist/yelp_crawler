from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from DataProviders import DataProviderService

from Models import Business

class BusinessDataProvider:
	def __init__(self):
		self.session = DataProviderService.getSession()
