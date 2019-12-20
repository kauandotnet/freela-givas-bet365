# coding=utf-8
import datetime
from sqlalchemy import Column, String, Integer, Date, Text, Boolean
from sqlalchemy import Numeric, Sequence, CHAR, DateTime, UniqueConstraint
from business.base import Base

class Fixture(Base):
    __tablename__ = 'Fixture'

    idFixture = Column(Integer, primary_key=True)
    description = Column(String(500), nullable=False)
    dateDescription = Column(String(50), nullable=False)
    time = Column(DateTime, default=datetime.datetime.now(), nullable=False)
    idCompetition = Column(Integer, nullable=False)
    idChallenge = Column(Integer, nullable=False)

    #RELATION
    #partidas
