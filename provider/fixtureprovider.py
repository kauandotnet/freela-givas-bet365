import json
import operator
from datetime import date, datetime
from sqlalchemy import func
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import or_

from business.base import Base
from business.fixture import Fixture
import config as cfg

class FixtureProvider:
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
            if(not self.session):
                session = self.create_session()
            encontrado = session.query(Fixture).filter_by(idFixture=objectData.idFixture).first()
            if(encontrado is None):
                result = self.inserir(objectData)

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

    def retornaListaFixturesPorCompeticaoPeriodo(self, idCompetition, dataInicio, dataFim):
        try:
            session = self.create_session()
            return session.query(Fixture)\
                .filter(Fixture.idCompetition == idCompetition).all()
                #.filter(Fixture.time <= datetime.now)\
                
        finally:
            session.close()          

    # def retornaPorStatusETipo(self, statusList, tipoConsulta):
    #     try:
    #         session = self.create_session()
    #         return session.query(Requisicao)\
    #         .filter(Requisicao.status.in_(statusList))\
    #         .filter(Requisicao.tipoConsulta == tipoConsulta)\
    #         .all()
    #     finally:
    #         session.close()            

