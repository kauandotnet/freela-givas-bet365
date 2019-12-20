import json
import operator
from datetime import date, datetime
from sqlalchemy import func
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import or_

from business.base import Base
from business.adversary import Adversary
from provider.baseprovider import BaseProvider
import config as cfg

class AdversaryProvider():
    def __init__(self, session=None):
        if(not session):
            self.session = session

    def create_session(self):
        engine = create_engine(cfg.conexao_banco_ativa['mysql_conn'])
        Session = sessionmaker(bind=engine)
        return Session()         

    def atualizar(self, objectData):
        try:
            result = False
            self.session = self.create_session()
            encontrado = self.session.query(Adversary)\
                    .filter_by(name=objectData.name)\
                    .first()
            if(encontrado is None):
                result = self.inserir(objectData) is not None

            result = True     
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
            self.session =self.create_session()
            self.session.add(objectData)
            self.session.flush()   
            result = objectData.idAdversary    
            self.session.commit() 
        except Exception as ex:
            print('Falha ao inserir: ' + str(ex))
            raise ex
        finally:
            if(self.session is not None):     
                self.session.close()   
            return result

    def retornaTodos(self, removeDraw=False):
        try:
            self.session =self.create_session()
            query = self.session.query(Adversary)
            if(removeDraw):
                query = query.filter(Adversary.idAdversary != 7)
            return query.all()
        finally:
            if(self.session is not None):     
                self.session.close()       

    def retornaTodosPorNomes(self, listaNome):
        try:
            self.session =self.create_session()
            return self.session.query(Adversary)\
                    .filter(Adversary.name == listaNome).first()
        finally:
            if(self.session is not None):     
                self.session.close()              
