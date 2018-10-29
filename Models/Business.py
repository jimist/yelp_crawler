from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, Date, JSON
from sqlalchemy.orm import relationship
from Models.Model import Model
import random
from pyld import jsonld

import time

class User(Model):
	__tablename__ = 'businesses'
	id = Column(Integer, primary_key=True)
