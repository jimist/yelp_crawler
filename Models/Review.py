import random
import time

from pyld import jsonld
from sqlalchemy import (BOOLEAN, JSON, VARCHAR, Column, Date, ForeignKey,
                        Integer, Numeric, String)
from sqlalchemy.dialects.mysql import CHAR, MEDIUMINT, TINYINT
from sqlalchemy.orm import relationship

from Models.Model import Model


class Review(Model):
    __tablename__ = 'reviews'
    id=Column(Integer,primary_key=True)
    business_id=Column(CHAR(22))
    user_id=Column(Integer)
    rating=Column(VARCHAR(4))
    text=Column(VARCHAR(5000))
    date=Column(VARCHAR(11))
