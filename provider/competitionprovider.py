import json
import operator
from datetime import date, datetime
from sqlalchemy import func
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import or_

from business.base import Base
from business.competition import Competition
import config as cfg

class CompetitionProvider:
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
            encontrado = session.query(Competition).filter_by(idCompetition=objectData.idCompetition).first()
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

    def retornaTodos(self, idSport=None):
        try:
            my_filters = {}
            session = self.create_session()
            query = session.query(Competition)
            if(idSport is not None):
                my_filters['idSport'] = idSport       

            for attr,value in my_filters.items():
                query = query.filter(getattr(Competition, attr) == value)
            return query.all()
        finally:
            session.close()

    def retornaPorAlternativeDescricao(self, altDescription):
        try:
            session = self.create_session()
            return session.query(Competition)\
                    .filter_by(alternativeDescription=altDescription).first()
        finally:
            session.close()

    # def atualizarStatus(self, cpf, entidade, statusNovo, obs=''):
    #     try:
    #         result = False
    #         session = self.create_session()
    #         encontrado = session.query(Requisicao).filter_by(cpf=cpf.strip(), entidade=entidade.strip()).first()
    #         if(encontrado is not None):
    #             print('ALTERANDO STATUS PARA NOVO...{}'.format(statusNovo))
    #             encontrado.status = statusNovo
    #             encontrado.observacao = obs
    #             encontrado.dataAtualizacao = datetime.now()
    #             session.commit()   
    #         result = True     
    #     except Exception as ex:
    #         print('ex: ' + str(ex))
    #         raise ex
    #     finally:
    #         session.close() 
    #         return result

    # def excluir(self, idRequisicao):
    #     try:
    #         session = self.create_session()
    #         regFound = session.query(Requisicao).filter_by(idRequisicao=idRequisicao).one()
    #         session.delete(regFound)
    #         session.commit()
    #     finally:
    #         session.close() 

    # def retornaPorId(self, idRequisicao):
    #     try:
    #         session = self.create_session()
    #         return session.query(Requisicao).filter_by(idRequisicao=idRequisicao).first()
    #     finally:
    #         session.close()

    # def retornaPorStatus(self, statusList):
    #     try:
    #         session = self.create_session()
    #         return session.query(Requisicao).filter(Requisicao.status.in_(statusList)).all()
    #     finally:
    #         session.close()

    # def retornaPorStatusETipo(self, statusList, tipoConsulta):
    #     try:
    #         session = self.create_session()
    #         return session.query(Requisicao)\
    #         .filter(Requisicao.status.in_(statusList))\
    #         .filter(Requisicao.tipoConsulta == tipoConsulta)\
    #         .all()
    #     finally:
    #         session.close()            

    # def retornaPorCpfEntidade(self, cpf, entidade, statusRegistro=None):
        # try:
        #     session = self.create_session()
        #     if(statusRegistro is None):
        #         return session.query(Requisicao)\
        #         .filter(Requisicao.cpf == cpf)\
        #         .filter(Requisicao.entidade == entidade)\
        #         .first()
        #         #.filter_by(cpf=cpf.strip(), entidade=entidade.strip()).first()
        #     else:
        #         return session.query(Requisicao).filter_by(cpf=cpf.strip(), entidade=entidade.strip(), \
        #                                                 status=statusRegistro.strip()).first()
        # finally:
        #     session.close()            