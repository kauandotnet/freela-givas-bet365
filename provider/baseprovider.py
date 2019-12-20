import json
import operator
from datetime import date, datetime
from sqlalchemy import func
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import or_, and_

from business.base import Base
from business.matchdata import MatchData
import config as cfg

class BaseProvider:
    def __init__(self, session=None, connectionName=None):
        self.session = session
        self.connectionName = connectionName if connectionName is not None else cfg.conexao_banco_ativa['mysql_conn']

    def create_session(self):    
        if(self.session is None):
            engine = create_engine(self.connectionName)
            Session = sessionmaker(bind=engine)
            return Session()            