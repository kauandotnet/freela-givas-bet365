import json
import operator
from datetime import date, datetime
from sqlalchemy import func
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import or_

from business.base import Base
from business.market import Market
import config as cfg

class MarketProvider:
    def __init__(self, session=None):
        if(not session):
            self.session = session

    def create_session(self):
        engine = create_engine(cfg.conexao_banco_ativa['mysql_conn'])
        Session = sessionmaker(bind=engine)
        return Session()

    def retornaTodosPorEsporte(self, idSport):
        try:
            session = self.create_session()
            return session.query(Market)\
                .filter(Market.idSport == idSport).all()
        finally:
            session.close()          

    def retornaMarketPorNome(self, name):
        try:
            session = self.create_session()
            return session.query(Market)\
                .filter(Market.name == name).first()
        finally:
            session.close()          


