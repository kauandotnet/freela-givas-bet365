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
from provider.adversaryprovider import AdversaryProvider
import config as cfg

class MatchDataProvider:
    def __init__(self, session=None):
        if(not session):
            self.session = session

    def create_session(self):
        engine = create_engine(cfg.conexao_banco_ativa['mysql_conn'], connect_args={'connect_timeout': 50})
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
                if(objectData.halfTimeResult is not None):
                    encontrado.halfTimeResult = objectData.halfTimeResult
                if(objectData.idAdversaryScoreFirst is not None):
                    encontrado.idAdversaryScoreFirst = objectData.idAdversaryScoreFirst                
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
    
    def atualizarResultados(self, idMatchData, matchResult, sumScore):
        try:
            result = None
            if(not self.session):
                self.session = self.create_session()

            encontrado = self.session.query(MatchData)\
                .filter(MatchData.idMatchData == idMatchData)\
                .first()
            if(encontrado is not None):
                encontrado.matchResult = matchResult                    
                encontrado.sumScore = sumScore
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

    def retornaTodos(self, idCompetition):
        try:
            result = None
            self.session = self.create_session()
            result = self.session.query(MatchData).all()
        finally:
            if(self.session is not None):     
                self.session.close()    
            return result

    def retornaPorData(self, idCompetition, date):
        try:
            result = None
            self.session = self.create_session()            
            result = self.session.query(MatchData)\
                .filter(MatchData.idCompetition == idCompetition)\
                .filter(MatchData.date == date).first()
        finally:
            if(self.session is not None):     
                self.session.close()   
            return result

    def retornaListaFixturesPorCompeticaoPeriodo(self, idCompetition, 
                                                dataInicio, dataFim):
        try:
            result = None
            self.session = self.create_session()
            result = self.session.query(MatchData)\
                .filter(MatchData.idCompetition == idCompetition)\
                .filter(MatchData.date >= dataInicio,\
                        MatchData.date < dataFim).all()
        finally:
            if(self.session is not None):     
                self.session.close()  
            return result 

    def consultaUltimosJogosPorLimite(self, idCompetition, qtdJogos=None, idAdversary=None,):
        try:
            result = None
            self.session = self.create_session()
            query = self.session.query(MatchData).filter(MatchData.idCompetition == idCompetition)
            if(idAdversary is not None):
                query = query.filter(or_(MatchData.idAdversary1 == idAdversary,\
                            MatchData.idAdversary2 == idAdversary))

            query =  query.filter(and_(MatchData.idWinner.isnot(None),\
                            MatchData.matchResult.isnot(None)))\
            .order_by(MatchData.date.desc())\
            
            if(qtdJogos is not None):
                query = query.limit(qtdJogos)
            
            result = query.all()
        finally:
            if(self.session is not None):     
                self.session.close()  
            return result

    def consultaUltimosJogosPorLimiteEntreSdversarios(self, idCompetition, qtdJogos=None, 
                                                    idAdversary1=None, idAdversary2=None):
        try:
            result = None
            self.session = self.create_session()
            query = self.session.query(MatchData).filter(MatchData.idCompetition == idCompetition)
            if(idAdversary1 is not None and idAdversary2 is not None):
                query = query.filter(and_(MatchData.idAdversary1 == idAdversary1,\
                                        MatchData.idAdversary2 == idAdversary2))

            query =  query.filter(and_(MatchData.idWinner.isnot(None),\
                            MatchData.matchResult.isnot(None)))\
            .order_by(MatchData.date.desc())\
            
            if(qtdJogos is not None):
                query = query.limit(qtdJogos)
            
            result = query.all()
        finally:
            if(self.session is not None):     
                self.session.close()  
            return result

    def consultaTodosJogosValidosPorPeriodo(self, idCompetition, inicio=None, fim=None):
        try:
            result = None
            self.session = self.create_session()
            query = self.session.query(MatchData).filter(MatchData.idCompetition == idCompetition)
            query = query.filter(and_(MatchData.idWinner.isnot(None),\
                            MatchData.matchResult.isnot(None)))
            if(inicio is not None and inicio is not None):
                query = query.filter(MatchData.date >= inicio,\
                                        MatchData.date < fim)
            result = query.order_by(MatchData.date.asc()).all()
        finally:
            if(self.session is not None):     
                self.session.close()          
            return result

    def consultaProximosJogos(self, idCompetition):
        try:            
            self.session = self.create_session()
            query = self.session.query(MatchData).filter(MatchData.idCompetition == idCompetition)
            return query.filter(and_(
                                MatchData.idWinner.is_(None),\
                                MatchData.matchResult.is_(None),\
                                MatchData.sumScore.is_(None)\
                            ))\
                .order_by(MatchData.date.desc())\
                .limit(6)\
                .all()
        finally:
            if(self.session is not None):     
                self.session.close()     

    def retornaMaximaHistoricaSemEmpate(self, idCompetition):
        maxima = -1
        contador = 0
        advProv = AdversaryProvider()
        drawCompetition = advProv.retornaIdEmpate(idCompetition)
        listaJogos = self.consultaTodosJogosValidosPorPeriodo(idCompetition, None, None)
        for jogo in listaJogos:        
            if(jogo.idWinner != drawCompetition.idAversary):
                contador += 1
            elif(jogo.idWinner == drawCompetition.idAversary):
                if(contador > maxima and contador not in [0, 1]):
                    maxima = contador
                contador = 0
        return maxima