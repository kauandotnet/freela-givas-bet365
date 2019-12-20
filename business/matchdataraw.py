# coding=utf-8
import datetime
from sqlalchemy import Column, String, Integer, Date, Text, Boolean
from sqlalchemy import Numeric, Sequence, CHAR, DateTime, UniqueConstraint
from business.base import Base

class MatchDataRaw(Base):
    __tablename__ = 'MatchDataRaw'

    idMatchDataRaw = Column(Integer, primary_key=True)
    matchMarkets = Column(Text(5000), nullable=True)
    
    date = Column(DateTime, default=datetime.datetime.now())
    idFixture = Column(Integer, nullable=False)
    idCompetition = Column(Integer, nullable=False)
    idChallenge = Column(Integer, nullable=False)
    
    #RELATION
