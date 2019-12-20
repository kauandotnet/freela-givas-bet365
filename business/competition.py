# coding=utf-8
import datetime
from sqlalchemy import Column, String, Integer, Date, Text, Boolean
from sqlalchemy import Numeric, Sequence, CHAR, DateTime, UniqueConstraint
from business.base import Base

class Competition(Base):
    __tablename__ = 'Competition'

    idCompetition = Column(Integer, primary_key=True)
    description = Column(String(20), nullable=False)
    alternativeDescription = Column(String(20), nullable=True)

    #RELATION


