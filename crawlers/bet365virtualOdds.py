import json
import locale
import math
import os
import re
import ssl
import sys
import time
import unicodedata
import datetime as dtime
from datetime import datetime, date
from decimal import Decimal
from multiprocessing.dummy import Pool as ThreadPool
from urllib.request import urlopen

import lxml
import lxml.html
import util
import calendar
import schedule
import logging
import calendar
import requests
import dashtable
import logaugment
import urllib.request
from ftfy import fix_encoding, fix_text, fix_text_encoding
from lxml import etree
from dateutil import relativedelta

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pymongo import MongoClient

import config as cfgPadrao
import business.extrator as dataExt
from business.market import Market
from business.fixture import Fixture
from business.matchdata import MatchData
from business.matchodds import MatchOdds
from business.competition import Competition
from provider.marketprovider import MarketProvider
from provider.fixtureprovider import FixtureProvider
from provider.adversaryprovider import AdversaryProvider
from provider.matchdataprovider import MatchDataProvider
from provider.matchoddsprovider import MatchOddsProvider
from provider.competitionprovider import CompetitionProvider
from crawlers.bet365virtual import CrawlerBet365Virtual
import crawlers.configs.bet365virtualodds_config as cfgEspecifico
from business.base import Session

class CrawlerBet365VirtualOdds(CrawlerBet365Virtual):
    def __init__(self, flagAction):
        super().__init__(False)
        if(not flagAction):
            return
        try:
            sucessoLogin = False
            self.dominio = cfgEspecifico.configParams['DOMAIN']
            self.urlDominio = cfgEspecifico.urls['SITE_DOMAIN']            
            self.browserSession = None
            self.listaMemoriaCompeticoes = []
            self.listaMemoriaMarkets = []
            adsProv = AdversaryProvider()
            self.listaAdversarys = adsProv.retornaTodos()
            
            logging.basicConfig(
                                format='%(asctime)s -- %(custom_key)s -- %(name)s - %(levelname)s - %(message)s', 
                                level=logging.INFO,
                                handlers=[
                                    logging.FileHandler(f"log/{self.dominio}.log", mode="w"),
                                    logging.StreamHandler()
                                ])
            self.logger = logging.getLogger()
            logaugment.set(self.logger, custom_key='N/A')

            # dbConKey = 'PROD' if 'localhost' not in cfgPadrao.database['mysql_conn'] else 'DESE'
            # self.logger.info(f'@@@ BANCO DE DADOS: {dbConKey}')
            try:                
                self.startChrome()                
                self.GetRequest(cfgEspecifico.urls['SITE_DOMAIN'])
                sucessoLogin = True 
                if(sucessoLogin):
                    self.fecharModalMensagem()
                    
                    TIMER = cfgPadrao.configParams['TIMER_ODDS']
                    while True:          
                        try:              
                            self.processaCapturaOdds()
                        except Exception as ex:
                            self.logger.error('Erro na captura das odds, sera reiniciado:' + str(ex))
                        time.sleep(TIMER)
                else:
                    self.logger.info('Não foi possivel efetuar o login.')                                   
            except Exception as fe:
                self.logger.error('Erro em CrawlerBet365VirtualOdds:' + str(fe))
            finally:
                self.logger.info('')
                self.logger.info('=================== ')
                self.logger.info('')
        except Exception as ex:
            print('ERRO --> ' + str(ex))
    
    def buscaCompeticaoMarket(self, nameMarket):
        marketProv = MarketProvider()
        if(len(self.listaMemoriaMarkets) == 0):
            self.listaMemoriaMarkets = marketProv.retornaTodosPorEsporte(idSport=1)   
        
        idMarket = next((c.idMarket for c in self.listaMemoriaMarkets if c.name == nameMarket), None) 
        return idMarket

    def processaCapturaOdds(self):
        self.logger.info('')
        self.logger.info('===============================================')
        self.logger.info(f'Processando captura de odds de Futebol Virtual')
        self.logger.info('===============================================')
        objLnkMenuEspVirt = self.GetElementObject(cfgEspecifico.html_xpaths['LNK_MENU_ESP_VIRTUAIS'])
        if(not objLnkMenuEspVirt):
            self.logger.info('Menu Esportes Virtuais não localizado')
            return

        #MENU LATERAL
        self.logger.info('Link Esportes Virtuais do menu lateral localizado.')
        self.scrollElementIntoView(objLnkMenuEspVirt, 100)
        self.sleep(1)
        objLnkMenuEspVirt.click()
        self.logger.info('Link clicado.')
        self.sleep(1)

        #SUBMENU
        self.logger.info('Buscando submenu Futebol...')
        objLnkSubmenuFutebol = self.GetElementObject(cfgEspecifico.html_xpaths['LNK_SUBMENU_FUTEBOL'])
        objLnkSubmenuFutebol.click()
        self.logger.info('Submenu Futebol clicado...')
        self.sleep(1)

        #PARA CADA COMPETICAO
        objLnkCompeticoes = self.GetAllElementObject(cfgEspecifico.html_xpaths['LST_COMPETITIONS'])
        for lnkCompetition in objLnkCompeticoes:
            self.logger.info('')
            self.logger.info('***********************************')
            nameCompetition = self.getTextoElemento(lnkCompetition)
            if(nameCompetition != cfgEspecifico.configParams['PROCESSA_ID_COMPETITION'][2]):
                continue
            self.logger.info(f'Processando competicao :{nameCompetition}')
            #BUSCA ID COMPETITION
            compProv = CompetitionProvider()
            competitionFound = compProv.retornaPorAlternativeDescricao(nameCompetition.strip())
            if(competitionFound is None):
                self.logger.error(f'Competicao com nome {nameCompetition} nao encontrada.')
                continue
            idCompetition = competitionFound.idCompetition
            if(idCompetition != cfgEspecifico.configParams['PROCESSA_ID_COMPETITION'][0]):
                continue
            
            lnkCompetition.click()
            self.sleep(1)

            #LISTA HORARIOS 6 PARTIDAS 
            self.logger.info('Buscando links das proximas partidas...')  

            #CAPTURA ODDS PELO HORARIO
            for index in range(1, 7):                
                linkPartida = self.GetElementObject(cfgEspecifico.html_xpaths['LNK_LISTA_PARTIDAS'].format(index))
                horario = self.getTextoElemento(linkPartida)
                if(linkPartida.is_enabled() and linkPartida.is_displayed()):
                    linkPartida.click()

                objRaceInfo = self.GetElementObject(cfgEspecifico.html_xpaths['DIV_RACE_INFO'])                
                objPartidaAtiva = self.GetChildElementObject(objRaceInfo, cfgEspecifico.html_xpaths['TXT_NOME_PARTIDA_ATIVA'])
                titulo = self.getTextoElemento(objPartidaAtiva)
                self.logger.info(f'Verificando odds da partida: Horario:{horario} -- Nome: {titulo}')

                objEventoIniciado = self.GetChildElementObject(objRaceInfo, cfgEspecifico.html_xpaths['TXT_EVENTO_INICIADO'])
                if(objEventoIniciado):
                    self.logger.info('Este evento foi iniciado, odds não disponiveis.')
                    continue
                
                matchDataProv = MatchDataProvider()
                matchOddsProv = MatchOddsProvider()
                datetimeOdd = self.montaDataOdd(horario)
                
                if(datetimeOdd is None):
                    continue
                
                firstTimeSave = False
                self.logger.info('Buscando dados de partidas no banco...')
                matchData = matchDataProv.retornaPorData(idCompetition, datetimeOdd)
                if(matchData is None): 
                    self.logger.info(f'Objeto MatchData não existe no banco DateTime:{datetimeOdd} - idCompetition:{idCompetition}!!!')
                    matchDataNew = MatchData()  
                    matchDataNew.title = titulo
                    matchDataNew.date  = datetimeOdd
                    matchDataNew.idCompetition = idCompetition
                    matchDataNew.idWinner = None
                    adversary1, adversary2 = dataExt.extrairAdversarios(titulo)
                    matchDataNew.idAdversary1 = self.retornaDadosAdversarioPorNome(adversary1, idCompetition)
                    matchDataNew.idAdversary2 = self.retornaDadosAdversarioPorNome(adversary2, idCompetition)
                    idMatchData = matchDataProv.atualizar(matchDataNew)
                    firstTimeSave = True
                else:
                    self.logger.info(f'Objeto MatchData já existe no banco idMatchData:{matchData.idMatchData} - idCompetition:{idCompetition}!!!')
                    idMatchData = matchData.idMatchData
                
                listaOddsGeradas = self.retornaListaOdds(idMatchData, datetimeOdd)
                if(firstTimeSave):
                    self.logger.info('Salvando as odds em lote...')
                    matchOddsProv.inserirBulk(listaOddsGeradas)
                else:
                    for odds in listaOddsGeradas:
                        self.logger.info(f'IdMatchData:{odds.idMatchData} -- IdMarket: {odds.idMarket} --> Name:{odds.name} - Value:{odds.value}')
                        matchOddsProv.atualizar(odds)                                                          
                time.sleep(1)

            self.logger.info('***********************************')

    def retornaListaOdds(self, idMatchData, datetimeOdd):
        result = []
        listaGruposOdds = self.GetAllElementObject(cfgEspecifico.html_xpaths['LST_GRUPO_ODDS'])
        for grupoOdds in listaGruposOdds:
            objGrupoNome = self.GetChildElementObject(grupoOdds, cfgEspecifico.html_xpaths['GRUPO_NOME'])
            nomeGrupoRaw = self.getTextoElemento(objGrupoNome)
            hashGrupo = nomeGrupoRaw.lower().replace(' ','')
            if(hashGrupo in ['vencedordojogo', 'númerodegols', 'timeamarcarprimeiro',
            'paraambosostimesmarcarem', 'paraotimedacasamarcar', 'paraotimevisitantemarcar']):                    
                self.logger.info('')
                self.logger.info('-------------------------------------')
                self.logger.info(f'-->> Nome grupo: {nomeGrupoRaw}')
                objContainerCelulas = self.GetAllChildElementObject(grupoOdds, cfgEspecifico.html_xpaths['CONTAINER_CELULA'])

                for celula in objContainerCelulas:
                    celulaNome = self.GetChildElementObject(celula, cfgEspecifico.html_xpaths['CELULA_TITLE'])
                    celulaValor = self.GetChildElementObject(celula, cfgEspecifico.html_xpaths['CELULA_VALUE'])
                    nome = self.getTextoElemento(celulaNome)
                    valor = self.getTextoElemento(celulaValor)
                    if(nome.strip() == '' or valor.strip() == ''):
                        continue
                    
                    self.logger.info(f'Titulo: {nome} -- Valor: {valor} -- DatetimeOdd:{datetimeOdd}')
                    odds = MatchOdds()                            
                    odds.name = nome
                    odds.value = valor                            
                    odds.idMatchData = idMatchData
                    odds.idMarket = self.buscaCompeticaoMarket(nomeGrupoRaw)
                    if(odds.idMarket is not None):
                            result.append(odds)
            elif(hashGrupo in ['resultadocorreto', 'intervalo-resultadocorreto', 'totaldegols']): 
                self.logger.info('')
                self.logger.info('-------------------------------------')
                self.logger.info(f'Nome grupo: {nomeGrupoRaw}')              
                objGrupoListaColunas = self.GetAllChildElementObject(grupoOdds, cfgEspecifico.html_xpaths['LST_GRUPO_COLUMNS'])  
                for colunaGrupo in objGrupoListaColunas:   
                    objGrupoHeader = self.GetChildElementObject(colunaGrupo, cfgEspecifico.html_xpaths['COLUMN_HEADER'])  
                    headerColuna = self.getTextoElemento(objGrupoHeader)
                    if(headerColuna == '' or headerColuna is None):
                        continue

                    self.logger.info(f'Header da coluna - {headerColuna}') 
                    objListaContainerColuna = self.GetAllChildElementObject(colunaGrupo, cfgEspecifico.html_xpaths['CONTAINER_CELULA'])
                    for index, celula in enumerate(objListaContainerColuna): 
                        objCelulaSpan1 = self.GetChildElementObject(celula, cfgEspecifico.html_xpaths['CELULA_TITLE'])
                        objCelulaSpan2 = self.GetChildElementObject(celula, cfgEspecifico.html_xpaths['CELULA_VALUE'])   
                        nameCell = None
                        valueCell = None 
                        if(hashGrupo == 'totaldegols'):
                            nameCell = str(index + 0.5)
                            valueCell = self.getTextoElemento(objCelulaSpan1)
                        else:
                            nameCell = self.getTextoElemento(objCelulaSpan1)
                            valueCell = self.getTextoElemento(objCelulaSpan2)

                        if(nameCell.strip() == '' or valueCell.strip() == ''):
                            self.logger.warning('Campo nome/valor da celula está vazio. Indo para próxima celula...')
                            continue
                        self.logger.info(f'Titulo: {nameCell} -- Valor: {valueCell} -- DatetimeOdd:{datetimeOdd}')
                        odds = MatchOdds()                            
                        odds.name = nameCell
                        odds.value = valueCell         
                        odds.columnHeader = headerColuna                    
                        odds.idMatchData = idMatchData
                        odds.idMarket = self.buscaCompeticaoMarket(nomeGrupoRaw)
                        if(odds.idMarket is not None):
                            result.append(odds)

        return result

    def montaDataOdd(self, horario):
        try:
            hora = int(horario.split(':')[0])
            minutos = int(horario.split(':')[-1])
            dataGerada = datetime(datetime.utcnow().year, datetime.utcnow().month, datetime.utcnow().day, hora, minutos , 0)
            self.logger.info(f'HORARIO CAPTURADO DA TABELA: {dataGerada}')
            return None if dataGerada > datetime.now() + dtime.timedelta(hours=4) else dataGerada
        except Exception as ex:
            self.logger.error(f'Falha ao montar data da Odd: {ex}')
            return None