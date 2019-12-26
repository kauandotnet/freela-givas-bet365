# coding=utf-8
import datetime
from sqlalchemy import Column, String, Integer, Date, Text, Boolean
from sqlalchemy import Numeric, Sequence, CHAR, DateTime, UniqueConstraint, ForeignKey
from business.base import Base
from business.competition import Competition

class Adversary(Base):
    __tablename__ = 'Adversary'

    idAdversary = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    #RELATION
    idCompetition = Column(Integer, ForeignKey(Competition.idCompetition))
