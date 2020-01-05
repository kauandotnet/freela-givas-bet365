import json
import operator
from datetime import date, datetime
from sqlalchemy import func
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import or_

from business.base import Base
from business.maxima import Maxima
import config as cfg

class MaximaProvider:
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

            encontrado = self.session.query(Maxima)\
                .filter(Maxima.idMaxima == objectData.idMaxima)\
                .first()
            if(encontrado is None):
                result = self.inserir(objectData)           
            else:
                encontrado.broken = objectData.broken    
                if(not encontrado.broken):
                    encontrado.lastSequenceCount = objectData.lastSequenceCount         
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
            result = objectData.idMaxima
            self.session.commit()
        except Exception as ex:
            print('Falha ao inserir: ' + str(ex))
            raise ex
        finally:
            if(self.session is not None):     
                self.session.close()  
            return result

    def retornaPorTypeMarket(self, idCompetition, idTypeMarket, broken=None):
        try:
            session = self.create_session()
            query = session.query(Maxima)\
                .filter(Maxima.idCompetition == idCompetition)\
                .filter(Maxima.idTypeMarket == idTypeMarket)
            if(broken is not None):
                query = query.filter(Maxima.broken == broken)
            return query.order_by(Maxima.date.desc()).first()
        finally:
            session.close()          




