import json
import operator
from datetime import date, datetime
from sqlalchemy import func
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import or_

from business.base import Base
from business.matchodds import MatchOdds
import config as cfg

class MatchOddsProvider:
    def __init__(self, session=None):
        if(not session):
            self.session = session

    def create_session(self):
        engine = create_engine(cfg.conexao_banco_ativa['mysql_conn'])
        Session = sessionmaker(bind=engine)
        return Session()

    def inserirBulk(self, listaObjetos):
        try:
            if(not self.session):
                self.session = self.create_session()
            self.session.bulk_save_objects(listaObjetos)
            self.session.commit()
        except Exception as ex:
            print('ex: ' + str(ex))
            raise ex
        finally:
            self.session.close()

    def atualizar(self, objectData):
        try:
            result = False
            if(not self.session):
                session = self.create_session()
            encontrado = session.query(MatchOdds)\
                .filter(MatchOdds.idMatchData == objectData.idMatchData)\
                .filter(MatchOdds.idMarket == objectData.idMarket)\
                .filter(MatchOdds.name == objectData.name).first()
            if(encontrado is None):
                result = self.inserir(objectData)
            else:
                encontrado.value = objectData.value
                
            result = True     
        except Exception as ex:
            print('ex: ' + str(ex))
            raise ex
        finally:
            session.close() 
            return result

    def inserir(self, objectData):
        try:
            result = False
            if(not self.session):
                session = self.create_session()
            session.add(objectData)
            session.commit()   
            result = True     
        except Exception as ex:
            print('Falha ao inserir: ' + str(ex))
            raise ex
        finally:
            session.close() 
            return result
