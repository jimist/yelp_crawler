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
from sqlalchemy.dialects.mysql import TINYINT,MEDIUMINT,CHAR,MEDIUMTEXT
from Models.Model import Model
import random
from pyld import jsonld

import time

class YelpUser(Model):
    __tablename__ = 'users'
    id=Column(Integer,primary_key=True)
    yelp_id=Column(VARCHAR(22))
    image_url=Column(VARCHAR(150))
    image_path=Column(VARCHAR(100))
    name=Column(VARCHAR(100))
    tagline=Column(VARCHAR(300))
    location=Column(VARCHAR(200))
    friends_count=Column(VARCHAR(5))
    reviews_count=Column(VARCHAR(6))
    photos_count=Column(VARCHAR(6))
    meta=Column(MEDIUMTEXT)