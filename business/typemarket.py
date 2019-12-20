# coding=utf-8
import datetime
from sqlalchemy import Column, String, Integer, Date, Text, Boolean
from sqlalchemy import Numeric, Sequence, CHAR, DateTime, UniqueConstraint, ForeignKey
from business.base import Base
from business.market import Market

class TypeMarket(Base):
    __tablename__ = 'TypeMarket'

    idTypeMarket = Column(Integer, primary_key=True)
    label = Column(String(50), default=False, nullable=False)
