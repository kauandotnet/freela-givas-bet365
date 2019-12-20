# coding=utf-8
import datetime
from sqlalchemy import Column, String, Integer, Date, Text, Boolean
from sqlalchemy import Numeric, Sequence, CHAR, DateTime, UniqueConstraint, ForeignKey
from business.base import Base
from business.sport import Sport

class Market(Base):
    __tablename__ = 'Market'

    idMarket = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    
    #RELATION
    idSport = Column(Integer, ForeignKey(Sport.idSport))    