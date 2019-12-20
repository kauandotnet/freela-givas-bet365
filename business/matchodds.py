# coding=utf-8
import datetime
from sqlalchemy import Column, String, Integer, Date, Text, Boolean
from sqlalchemy import Numeric, Sequence, CHAR, DateTime, UniqueConstraint, ForeignKey
from business.base import Base
from business.matchdata import MatchData
from business.market import Market

class MatchOdds(Base):
    __tablename__ = 'MatchOdds'

    idMatchOdds = Column(Integer, primary_key=True)
    columnHeader = Column(String(50), nullable=True)
    name = Column(String(100), nullable=True)
    value = Column(Numeric(precision=10, scale=2))
    yes = Column(Numeric(precision=10, scale=2))
    no = Column(Numeric(precision=10, scale=2))
    date = Column(DateTime, default=datetime.datetime.now())
    
    #RELATION
    idMatchData = Column(Integer, ForeignKey(MatchData.idMatchData))    
    idMarket = Column(Integer, ForeignKey(Market.idMarket))    