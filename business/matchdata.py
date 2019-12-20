# coding=utf-8
import datetime
from sqlalchemy import Column, String, Integer, Date, Text, Boolean
from sqlalchemy import Numeric, Sequence, CHAR, DateTime, UniqueConstraint
from business.base import Base

class MatchData(Base):
    __tablename__ = 'MatchData'

    idMatchData = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    matchResult = Column(String(50), nullable=True)
    sumScore = Column(Integer, nullable=True)    
    date = Column(DateTime, default=datetime.datetime.now())
    
    #RELATION
    idWinner = Column(Integer, nullable=True)
    idAdversary1 = Column(Integer, nullable=True)
    idAdversary2 = Column(Integer, nullable=True)

    idFixture = Column(Integer, nullable=True)
    idCompetition = Column(Integer, nullable=False)
    idChallenge = Column(Integer, nullable=True)
