# coding=utf-8
import datetime
from sqlalchemy import Column, String, Integer, Date, Text, Boolean
from sqlalchemy import Numeric, Sequence, CHAR, DateTime, UniqueConstraint, ForeignKey
from business.base import Base
from business.market import Market
from business.typemarket import TypeMarket

class Maxima(Base):
    __tablename__ = 'Maxima'

    idMaxima = Column(Integer, primary_key=True)
    broken = Column(Boolean, default=False, nullable=False)
    date = Column(DateTime, default=datetime.datetime.now())

    #RELATION
    idTypeMarket = Column(Integer, ForeignKey(TypeMarket.idTypeMarket))    