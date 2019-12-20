# coding=utf-8
import datetime
from sqlalchemy import Column, String, Integer, Date, Text, Boolean
from sqlalchemy import Numeric, Sequence, CHAR, DateTime, UniqueConstraint
from business.base import Base

class Sport(Base):
    __tablename__ = 'Sport'

    idSport = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
