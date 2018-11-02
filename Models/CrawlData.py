from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, DateTime, JSON
from Models.Model import Model
from sqlalchemy.dialects.mysql import MEDIUMTEXT
import datetime


class CrawlData(Model):
    __tablename__ = 'crawl_data'
    id = Column(Integer, primary_key=True)
    url = Column(String(256))
    body = Column(MEDIUMTEXT)
    requestHeader = Column(MEDIUMTEXT)
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
