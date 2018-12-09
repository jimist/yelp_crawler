from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    Numeric,
    Date,
    JSON,
    VARCHAR,
    BOOLEAN,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT,MEDIUMINT,CHAR
from Models.Model import Model
import random
from pyld import jsonld

import time


class Business(Model):
    __tablename__ = 'businesses'
    id = Column(CHAR(22), primary_key=True)
    name = Column(VARCHAR(100))
    address = Column(VARCHAR(200))
    city= Column(VARCHAR(200))
    latitude = Column(VARCHAR(40))
    longitude = Column(VARCHAR(40))
    stars = Column(VARCHAR(4))
    review_count = Column(MEDIUMINT)

