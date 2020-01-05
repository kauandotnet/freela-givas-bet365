# coding=utf-8
import datetime
from sqlalchemy import Column, String, Integer, Date, Text, Boolean
from sqlalchemy import Numeric, Sequence, CHAR, DateTime, UniqueConstraint, ForeignKey
from business.base import Base
from business.market import Market
from business.typemarket import TypeMarket
from business.competition import Competition

class Maxima(Base):
    __tablename__ = 'Maxima'

    idMaxima = Column(Integer, primary_key=True)
    broken = Column(Boolean, default=False, nullable=False)
    lastSequenceCount = Column(Integer, default=0, nullable=False)
    date = Column(DateTime, default=datetime.datetime.now())

    #RELATION
    idTypeMarket = Column(Integer, ForeignKey(TypeMarket.idTypeMarket), nullable=False)    
    idCompetition = Column(Integer, ForeignKey(Competition.idCompetition), nullable=False)