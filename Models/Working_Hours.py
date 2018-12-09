from sqlalchemy import (
    Column,
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


class Working_Hours(Model):
    __tablename__ = 'working_hours'
    biz_id=Column(CHAR(22),primary_key=True)
    monday = Column(VARCHAR(40))
    sunday = Column(VARCHAR(40))
    tuesday = Column(VARCHAR(40))
    wednesday = Column(VARCHAR(40))
    thursday = Column(VARCHAR(40))
    friday = Column(VARCHAR(40))
    saturday = Column(VARCHAR(40))