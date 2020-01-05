import json
import operator
from datetime import date, datetime
from sqlalchemy import func
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import or_

from business.base import Base
from business.typemarket import TypeMarket
import config as cfg

class TypeMarketProvider:
    def __init__(self, session=None):
        if(not session):
            self.session = session

    def create_session(self):
        engine = create_engine(cfg.conexao_banco_ativa['mysql_conn'])
        Session = sessionmaker(bind=engine)
        return Session()

    def atualizar(self, objectData):
        try:
            result = None
            if(not self.session):
                self.session = self.create_session()

            encontrado = self.session.query(TypeMarket)\
                .filter(TypeMarket.idTypeMarket == objectData.idTypeMarket)\
                .first()
            if(encontrado is None):
                result = self.inserir(objectData)           
            else:
                encontrado.date = datetime.now()
                encontrado.broken = objectData.broken            
                result = encontrado
            self.session.commit()
        except Exception as ex:
            print('ex: ' + str(ex))
            raise ex
        finally:       
            if(self.session is not None):     
                self.session.close() 
            return result

    def inserir(self, objectData):
        try:
            result = None
            if(not self.session):
                self.session = self.create_session()
            self.session.add(objectData)
            self.session.flush()   
            result = objectData.idTypeMarket    
            self.session.commit()
        except Exception as ex:
            print('Falha ao inserir: ' + str(ex))
            raise ex
        finally:
            if(self.session is not None):     
                self.session.close()  
            return result

    def retornaTodosPorMercado(self, idMarket):
        try:
            session = self.create_session()
            return session.query(TypeMarket)\
                .filter(TypeMarket.idMarket == idMarket).all()
        finally:
            session.close()          

    def retornaMarketPorLabel(self, label):
        try:
            session = self.create_session()
            return session.query(TypeMarket)\
                .filter(TypeMarket.label.like(label))\
                .first()
        finally:
            session.close()          


