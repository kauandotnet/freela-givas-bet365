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
from provider.baseprovider import BaseProvider
import config as cfg

class MatchDataProvider:
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

            encontrado = self.session.query(MatchData)\
                .filter(MatchData.idCompetition == objectData.idCompetition)\
                .filter(MatchData.date == objectData.date).first()
            if(encontrado is None):
                result = self.inserir(objectData)           
            else:
                encontrado.sumScore = objectData.sumScore
                if(objectData.matchResult is not None):
                    encontrado.matchResult = objectData.matchResult
                if(objectData.idWinner is not None):
                    encontrado.idWinner = objectData.idWinner                    
                if(objectData.idFixture is not None):
                    encontrado.idFixture = objectData.idFixture
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
            result = objectData.idMatchData     
            self.session.commit()
        except Exception as ex:
            print('Falha ao inserir: ' + str(ex))
            raise ex
        finally:
            if(self.session is not None):     
                self.session.close()  
            return result

    def retornaTodos(self):
        try:
            self.session = self.create_session()
            return self.session.query(MatchData).all()
        finally:
            if(self.session is not None):     
                self.session.close()        

    def retornaPorData(self, idCompetition, date):
        try:
            self.session = self.create_session()            
            return self.session.query(MatchData)\
                .filter(MatchData.idCompetition == idCompetition)\
                .filter(MatchData.date == date).first()
        finally:
            if(self.session is not None):     
                self.session.close()   

    def retornaListaFixturesPorCompeticaoPeriodo(self, idCompetition, 
                                                dataInicio, dataFim):
        try:
            self.session = self.create_session()
            return self.session.query(MatchData)\
                .filter(MatchData.idCompetition == idCompetition)\
                .filter(MatchData.date >= dataInicio,\
                        MatchData.date < dataFim).all()
        finally:
            if(self.session is not None):     
                self.session.close()  

    def consultaUltimosJogosSemEmpate(self, qtdJogos=None, idAdversary=None):
        try:
            self.session = self.create_session()
            query = self.session.query(MatchData)
            if(idAdversary is not None):
                query = query.filter(or_(MatchData.idAdversary1 == idAdversary,\
                            MatchData.idAdversary2 == idAdversary))

            query =  query.filter(and_(MatchData.idWinner.isnot(None),\
                            MatchData.matchResult.isnot(None)))\
            .order_by(MatchData.date.desc())\
            
            if(qtdJogos is not None):
                query = query.limit(qtdJogos)
            
            return query.all()
        finally:
            if(self.session is not None):     
                self.session.close()   

    def consultaTodosJogosValidos(self, inicio, fim):
        try:
            self.session = self.create_session()
            query = self.session.query(MatchData)
            return query.filter(and_(MatchData.idWinner.isnot(None),\
                            MatchData.matchResult.isnot(None)))\
            .filter(MatchData.date >= inicio,\
                    MatchData.date < fim)\
            .order_by(MatchData.date.asc())\
            .all()

        finally:
            if(self.session is not None):     
                self.session.close()                 