import json
import locale
import math
import ast
import os
import re
import ssl
import sys
import time
import _thread
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
from business.maxima import Maxima
from business.fixture import Fixture
from business.matchdata import MatchData
from business.adversary import Adversary
from business.competition import Competition
from business.typemarket import TypeMarket
from business.matchdataraw import MatchDataRaw
from provider.maximaprovider import MaximaProvider
from provider.fixtureprovider import FixtureProvider
from provider.typemarketprovider import TypeMarketProvider
from provider.adversaryprovider import AdversaryProvider
from provider.matchdataprovider import MatchDataProvider
from provider.matchdatarawprovider import MatchDataRawProvider
from provider.competitionprovider import CompetitionProvider
from crawlers.baseCrawlerSelenium import CrawlerSelenium
import crawlers.configs.bet365virtual_config as cfgEspecifico

class CrawlerBet365Virtual(CrawlerSelenium):
    def __init__(self, flagAction):
        super().__init__()
        if(not flagAction):
            return
        try:
            sucessoLogin = False
            self.sessionCookie = None
            self.browserSession = None
            self.dominio = cfgEspecifico.configParams['DOMAIN']
            self.urlDominio = cfgEspecifico.configParams['SITE_DOMAIN']            
            self.limitadorTempo = cfgEspecifico.configParams['INTERVALO_TEMPO']
            self.execucaoDiaria = cfgEspecifico.configParams['EXECUCAO_DIARIA']
            adsProv = AdversaryProvider()
            self.listaAdversarys = adsProv.retornaTodos()
            
            nomeLog = f'{self.dominio}_DIARIO' if self.execucaoDiaria else f'{self.dominio}_PERIODO'
            logging.basicConfig(
                                format='%(asctime)s -- %(custom_key)s - %(levelname)s - %(message)s', 
                                level=logging.INFO,
                                handlers=[
                                    logging.FileHandler(f"log/{nomeLog}.log", mode="w"),
                                    logging.StreamHandler()
                                ])
            logging.getLogger('schedule').propagate = False
            self.logger = logging.getLogger()
            logaugment.set(self.logger, custom_key='N/A')

            # dbConKey = 'PROD' if 'localhost' not in cfgPadrao.database['mysql_conn'] else 'DESE'
            # self.logger.info(f'@@@ BANCO DE DADOS: {dbConKey}')
            try:                
                self.logger.info('')
                self.logger.info('#############################')
                listaPeriodos = self.carregaPeriodos()
                self.logger.info(f'Total de períodos retornados: {len(listaPeriodos)}. Iniciando threads...') 
                for item in listaPeriodos:
                    self.logger.info(item)
                self.logger.info('#############################')
                self.logger.info('')
                
                self.startChrome()   
                sucessoLogin = self.efetuaLogin()
                if(sucessoLogin):
                    self.logger.info('Login efetuado com sucesso. Iniciando pesquisa...')
                    time.sleep(3)

                    self.carregaSessao()    
                    self.logger.info(f'Sessao pronta.')            
                    self.fecharModalMensagem()

                    def job():
                        self.logger.info(f'Filtrando resultados...')    
                        listaPeriodos = self.carregaPeriodos()    
                        if(len(listaPeriodos) > 0):
                            pool = ThreadPool(cfgPadrao.threads['MAX_COUNT'])
                            pool.map(self.processaDetalhes, listaPeriodos) 
                            pool.close()
                            pool.join()
                            self.logger.info('THREAD FINALIZADA.') 

                    #LOOP 3MIN
                    TIMER = cfgPadrao.configParams['TIMER']
                    if(TIMER == 0):
                        job()
                    else:
                        schedule.every(TIMER).seconds.do(job)

                    self.logger.info('Aguardando inicio do job...')
                    while True:                        
                        schedule.run_pending()
                else:
                    self.logger.info('Não foi possivel efetuar o login.')                                   
            except Exception as fe:
                self.logger.info('Erro na consulta:' + str(fe))
            finally:
                if(sucessoLogin):
                    time.sleep(3)
                    self.logger.info('Iniciando processo de logout...')
                    saiu = self.efetuaLogout()
                    if(saiu):
                        self.logger.info('Logout efetuado.')
                    else:
                        self.logger.info('Logout com problemas.')
                    time.sleep(2)
                self.logger.info('')
                self.logger.info('=================== ')
                self.logger.info('')
        except Exception as ex:
            print('ERRO --> ' + str(ex))
    
    def startChrome(self):
        chromeOptions = Options()
        #HEAD
        if(cfgEspecifico.configParams['EXECUTAR_MODO_HEADLESS']):
            self.logger.info('Executando crawler em modo HEADLESS.')
            chromeOptions.add_argument("--disable-extensions")
            chromeOptions.add_argument("--disable-gpu")
            chromeOptions.add_argument("--headless")
        #IMAGES
        # prefs = {"profile.managed_default_content_settings.images": 2}
        # chromeOptions.add_experimental_option("prefs", prefs)
        #EXTRA
        # chromeOptions.add_argument('--remote-debuggin-port=9222')
        #chromeOptions.add_experimental_option("excludeSwitches", ['enable-automation'])
        
        userAgent = cfgPadrao.configParams['USER_AGENT']
        chromeOptions.add_argument("--start-maximized")
        #chromeOptions.add_argument("window-size=1920,1080")
        chromeOptions.add_argument(f"--user-agent={userAgent}")
        
        capabilities = webdriver.DesiredCapabilities.CHROME
        capabilities["chrome.switches"] = [f"--user-agent={userAgent}"] 
        self.browserSession = webdriver.Chrome(chrome_options=chromeOptions, desired_capabilities=capabilities)

    def efetuaLogin(self):
        try:
            self.logger.info(f'$$$ Resolução viewport $$$ -- {self.browserSession.get_window_size()}')
            self.logger.info('Inciciando processo de login...')        
            self.GetRequest(cfgEspecifico.login_credenciais['URL_LANGUAGE'])
            self.GetRequest(cfgEspecifico.login_credenciais['URL_LOGIN'])
            self.logger.info('Tela de login aberta. Procurando componentes...')        
            time.sleep(1)

            sucesso = False
            tentativaLogin = 1
            while tentativaLogin <= 6:
                try:
                    time.sleep(2)
                    elementBoxUser = self.GetElementObject(cfgEspecifico.html_xpaths['LOGIN_BOX_USER']) 
                    elementBoxPass = self.GetElementObject(cfgEspecifico.html_xpaths['LOGIN_BOX_PASS'])     
                    self.logger.info(f'Situação componentes login: BoxUser:{elementBoxUser} -- BoxPass:{elementBoxPass}')
                    if(elementBoxUser and elementBoxPass):
                        self.logger.info('Componentes localizados. Informando credenciais...')
                        interactable = False
                        while not interactable:
                            try:
                                elementBoxUser = self.GetElementObject(cfgEspecifico.html_xpaths['LOGIN_BOX_USER']) 
                                elementBoxPass = self.GetElementObject(cfgEspecifico.html_xpaths['LOGIN_BOX_PASS'])
                                elementBoxUser.clear()
                                elementBoxPass.clear()
                                elementBoxUser.send_keys(cfgEspecifico.login_credenciais['USER_LOGIN'].strip())  
                                elementBoxUser.send_keys(Keys.TAB)
                                time.sleep(1)
                                elementBoxPass.send_keys(cfgEspecifico.login_credenciais['SENHA_LOGIN'].strip())                                
                                interactable = True
                            except ElementNotInteractableException:
                                self.logger.info('Aguardando componentes interagiveis...')
                                time.sleep(3)

                        time.sleep(1)                                                          
                        valorUserPreenchido = elementBoxUser.get_attribute("value").strip()
                        valorSenhaPreenchida = elementBoxPass.get_attribute("value").strip()
                        self.logger.info(f'Valor User Preenchido: {valorUserPreenchido}')
                        self.logger.info(f'Valor Senha Preenchida: {valorSenhaPreenchida}')

                        if(valorUserPreenchido == cfgEspecifico.login_credenciais['USER_LOGIN']
                         and valorSenhaPreenchida == cfgEspecifico.login_credenciais['SENHA_LOGIN']):
                            self.logger.info('Campos preenchidos. Botão de login clicado. Aguardando...')
                            elementBoxBtnOk = self.GetElementObject(cfgEspecifico.html_xpaths['LOGIN_BTN_OK'])
                            if(elementBoxBtnOk):
                                elementBoxBtnOk.click()
                                self.logger.info('Procurando menu superior e botão de SAIR...')
                                time.sleep(2)
                                elementLinkMenu = self.GetElementObject(cfgEspecifico.html_xpaths['LOGOUT_MENU'])                                  
                                if(elementLinkMenu):
                                    sucesso = True
                                    break
                        else:
                            self.logger.info('Os campos não preenchidos ou incorretos.')                                            
                    else:
                        self.logger.info('Componentes não localizados.')
                except Exception as ex:
                    self.logger.error(f'Falha: {ex} -- Nova tentativa de click em LOGIN em 5s...')
                    time.sleep(5)
                finally:
                    tentativaLogin += 1            
            return sucesso
        except Exception as ex:
            self.logger.error(f'Falha ao tentar efetuar o login. Detalhes: {ex}')
            return False

    def efetuaLogout(self):
        try:
            self.logger.info('Inciciando processo de logout...')        
            sucesso = False
            tentativaLogout = 1
            while tentativaLogout <= 3:
                try:
                    self.GetRequest(cfgEspecifico.login_credenciais['URL_LOGIN'])
                    time.sleep(3)
                    self.fecharModalMensagem()
                    time.sleep(3)
                    self.logger.info('Procurando menu superior e botão de SAIR...')
                    elementLinkMenu = self.GetElementObject(cfgEspecifico.html_xpaths['LOGOUT_MENU'])  
                    time.sleep(5)
                    if(elementLinkMenu):
                        self.logger.info('Menu localizado')
                        elementLinkMenu.click()
                        time.sleep(2)
                        elementLinkSair = self.GetElementObject(cfgEspecifico.html_xpaths['LOGOUT_LNK_SAIR'])
                        if(elementLinkSair):
                            self.logger.info('Botão SAIR localizado')
                            time.sleep(2)
                            elementLinkSair.click()
                            self.logger.info('Botão de SAIR clicado. Aguardando...')
                            sucesso = True
                        break
                    else:
                        self.logger.info('Componentes não localizados.')
                except Exception as ex:
                    self.logger.info('Nova tentativa de click em SAIR em 5s...')
                    time.sleep(5)
                finally:
                    tentativaLogout += 1            
            return sucesso
        except Exception as ex:
            self.logger.info(f'Falha ao tentar efetuar o logout. Detalhes: {ex}')
            return False

    def fecharModalMensagem(self):
        try:
            tentativas = 0
            modalAberto = True
            while(modalAberto and tentativas <= 5):
                elementModalFechar = self.GetElementObject(cfgEspecifico.html_xpaths['MODAL_MSG_LOGIN']) 
                if(elementModalFechar):
                    self.logger.info('Modal de mensagem detectado.')
                    elementModalFechar.click()
                    self.logger.info('Botão de fechar clicado.')
                    modalAberto = False
                    break
                time.sleep(1)
                tentativas += 1                
            return True
        except Exception as ex:
            self.logger.error(f'Falha ao tentar fechar o modal. Detalhes: {ex}')
            return False

    def carregaPeriodos(self):
        listaPeriodos = []
        sufixo = 'T03:00:00.000Z'
             
        fimPeriodo = None
        periodoProcessamento = cfgEspecifico.configParams['PROCESSA_POR_PERIODO']
        mesAtual = datetime.now().month
        #LAST 6 MONTHS 30DAYS/MONTH
        if(not self.execucaoDiaria):     
            rangeStart = None
            rangeEnd = None
            self.logger.info('Carregando periodo por mês.')   
            if(periodoProcessamento is not None and len(periodoProcessamento) > 0):
                self.logger.info('Periodo informado pelo usuario...') 
                minimo = periodoProcessamento[0]
                maximo = periodoProcessamento[1]
                inicioPeriodo = datetime(minimo[2], minimo[1], minimo[0], 3, 0 , 0)
                fimPeriodo = datetime(maximo[2], maximo[1], maximo[0], 3, 0 , 0)
                rangeStart = minimo[1]
                rangeEnd = maximo[1] + 1 if minimo[1] < maximo[1] else maximo[1] + 1
            else:
                self.logger.info('Periodo não informado pelo usuario. Processamento 6 meses...') 
                inicioPeriodo = datetime(datetime.now().year, mesAtual - 5, 1, 3, 0 , 0)
                fimPeriodo = datetime(datetime.now().year, mesAtual, datetime.now().day, 3, 0 , 0)
                rangeStart =  mesAtual - 5
                rangeEnd = mesAtual + 1
            
            countDias = (fimPeriodo - inicioPeriodo).days
            if countDias >= 28:
                faixaDias = 28  
            else:
                faixaDias = countDias

            for i in range(rangeStart, rangeEnd):        
                dataFimMes = inicioPeriodo + dtime.timedelta(days=faixaDias)
                if(fimPeriodo is None and dataFimMes > datetime.now()):
                    dataFimMes = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 3, 0 , 0)
                elif(dataFimMes > fimPeriodo):
                    dataFimMes = datetime(fimPeriodo.year, fimPeriodo.month, fimPeriodo.day, 3, 0 , 0)

                if(inicioPeriodo > fimPeriodo or inicioPeriodo > dataFimMes):
                    break

                inicio = '{0}-{1:02}-{2}{3}'.format(inicioPeriodo.year, inicioPeriodo.month, inicioPeriodo.day, sufixo)
                fim = '{0}-{1:02}-{2}{3}'.format(dataFimMes.year, dataFimMes.month, dataFimMes.day, sufixo)               
                listaPeriodos.append((inicio, fim))
                inicioPeriodo = dataFimMes + dtime.timedelta(days=1)                 
        else:
            self.logger.info('Carregando execução diária.')
            diaAtual = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 3, 0 , 0)
            listaPeriodos.append((diaAtual, diaAtual + dtime.timedelta(days=1)))
        return listaPeriodos

    def processaDetalhes(self, tuplaPeriodoData):
        try:
            self.logger.info('')
            self.logger.info('===========================================')
            self.logger.info(f'Processando período: {tuplaPeriodoData}.')
            self.logger.info('===========================================')
            idEsporte = cfgEspecifico.configParams['DATA_SPORT_ID_MYSQL']
            dataInicio = tuplaPeriodoData[0]
            dataFim = tuplaPeriodoData[1]

            #COMPETICOES
            listaCompeticoes = self.retornaCompeticoes(idEsporte, dataInicio, dataFim)
            limitadorNumComp = cfgEspecifico.configParams['LIMITE_COLETA_COMPETICAO']
            if(limitadorNumComp is not None):
                listaCompeticoes = listaCompeticoes[:limitadorNumComp]

            self.logger.info(f'Lista de competições encontradas: {len(listaCompeticoes)}.')        
            for competition in listaCompeticoes:
                idCompetition = competition.idCompetition
                logaugment.set(self.logger, custom_key=idCompetition)

                urlFixture = self.montarUrlFixture(idCompetition, dataInicio, dataFim)
                #FIXTURES
                listaFixtures = self.retornaFixtures(urlFixture)
                limitadorNumFix = cfgEspecifico.configParams['LIMITE_COLETA_FIXTURE']
                if(limitadorNumFix is not None):
                    listaFixtures = listaFixtures[:limitadorNumFix]

                self.logger.info(f'Lista de fixtures encontradas: {len(listaFixtures)}.')
                fixtureProv = FixtureProvider()
                matchdataProv = MatchDataProvider()
                matchdatarawProv = MatchDataRawProvider()

                #BUSCA AS FICTURES NO BANCO PARA ESTA COMPETICAO/PERIODO
                listaMatchFixturesTemp = matchdataProv.retornaListaFixturesPorCompeticaoPeriodo(idCompetition, dataInicio, dataFim)
                listaMatchFixturesExistentes = [f.idFixture for f in listaMatchFixturesTemp if f.idFixture is not None]
                self.logger.info(f'Qtd. Fixture/MatchData localizadas no banco: {len(listaMatchFixturesExistentes)}')

                for fixture in listaFixtures:
                    if(fixture.time < datetime.now() - dtime.timedelta(minutes=cfgEspecifico.configParams['DELTA_LIMITE_COLETA_DIARIA'])
                    and self.execucaoDiaria):
                        self.logger.info(f'A Fixture será desconsiderada pois é antiga. Time:{fixture.time}')
                        continue
                                        
                    if(fixture.idFixture in listaMatchFixturesExistentes):
                        self.logger.info(f'A Fixture/MatchData {fixture.idFixture} já existe no banco.')
                        continue

                    idFixture = fixture.idFixture
                    idChallenge = fixture.idChallenge
                    self.logger.info('-------------------------------------------')
                    self.logger.info(f'FIXTURE -->> IdFixture:{idFixture} -- Descricao:{fixture.description} -- Data: {fixture.dateDescription}')
                    fixtureProv.atualizar(fixture)

                    self.logger.info(f'Fixture gravada. Id Gerado: {idFixture}')
                    urlPartida = self.montarUrlResultadoPartida(idCompetition, dataInicio, dataFim, idFixture, idChallenge)
                    matchData, matchrawData, dicNomesTimes = self.retornaDadosPartida(urlPartida, idCompetition, idFixture, idChallenge)
                    if(matchData is not None and matchrawData is not None):
                        self.logger.info(f'PARTIDA -->> Vencedor:{matchData.idWinner} -- Resultado: {matchData.matchResult} -- Gols:{matchData.sumScore}')                            

                        matchResult = matchData.matchResult
                        halfTimeResult = matchData.halfTimeResult
                        idAdversary1 = matchData.idAdversary1
                        idAdversary2 = matchData.idAdversary2
                        idAdversaryScoreFirst = matchData.idAdversaryScoreFirst
                        matchMarketsRaw = matchrawData.matchMarkets
                        matchdataProv.atualizar(matchData)
                        matchdatarawProv.atualizar(matchrawData)   
                        _thread.start_new_thread(self.calculaMaximas,(matchMarketsRaw, idCompetition, matchResult, halfTimeResult,idAdversary1, idAdversary2, idAdversaryScoreFirst))

                    self.logger.info('-------------------------------------------')
                    self.sleep()
                self.sleep(cfgEspecifico.configParams['INTERVALO_TEMPO_COMPETICOES'])
                            
            return True
        except Exception as me:
            self.logger.error(f'Falha ao processar os detalhes: {me}.')

    def retornaCompeticoes(self, idEsporte, dataInicio, dataFim):
        comProv = CompetitionProvider()        
        return comProv.retornaTodos(idEsporte)

    def retornaCompeticoesExtraBet(self, idEsporte, dataInicio, dataFim):
        result = []
        compFixa = cfgEspecifico.configParams['PROCESSA_ID_COMPETITION']
        if(compFixa is not None):
            competition = Competition()
            competition.idCompetition = compFixa[0]
            competition.description = compFixa[1]
            return [competition]

        urlBase = cfgEspecifico.urls['URL_JSON_BASE_COMPETICOES']
        urlParams = urlBase.format(idEsporte, dataInicio, dataFim)
        listaJsonCompeticoes = self.carregaJsonTela(urlParams)
        for itemJson in listaJsonCompeticoes:
            competition = Competition()
            competition.idCompetition = util.getAtributo(itemJson, 'Id')
            competition.description = util.getAtributo(itemJson, 'Description')
            if(competition.idCompetition != '' and competition.description != ''):
                found = False
                for i in result:
                    if(i.idCompetition == competition.idCompetition):
                        found = True
                        break
                if(not found):
                    result.append(competition)
        self.logger.info('JSON competicoes carregado.')
        return result

    def retornaDadosPartida(self, url, idCompetition, idFixture, idChalenge):
        try:                        
            partidaRaw = MatchDataRaw()
            matchDataProv = MatchDataProvider()

            listaJson = self.carregaJsonTela(url)   
            dateAttJson = util.getAtributo(listaJson, 'date')
            dateMatch = datetime.strptime(dateAttJson, '%Y-%m-%dT%H:%M:%S')
            
            partida = matchDataProv.retornaPorData(idCompetition, dateMatch)
            if(partida is None): 
                partida = MatchData()
                partida.date = dateMatch
                partida.title = util.getAtributo(listaJson, 'title')
                
            partida.idFixture = idFixture 
            partida.idChallenge = idChalenge 
            partida.idCompetition = idCompetition
            partidaRaw.idCompetition = idCompetition  
            partidaRaw.idFixture = idFixture
            partidaRaw.idChallenge = idChalenge

            matchMarkets = util.getAtributo(listaJson, 'matchMarkets')
            partidaRaw.matchMarkets = str(matchMarkets)
            winner = ''
            adversary1 = ''
            adversary2 = ''
            matchResult = None
            for dado in matchMarkets:
                dado = dado.strip().lower()
                textoBase = self.extrairApostaVencedora(dado)
                if('vencedor da partida' in dado):
                    winner = dataExt.extrairVencedor(textoBase)
                    adversary1, adversary2 = dataExt.extrairAdversarios(partida.title)
                elif('resultado correto' in dado and 'grupo' not in dado and 'intervalo' not in dado):
                    matchResult = dataExt.extrairResultadoPartida(textoBase)     
                elif('número de gols' in dado):
                    partida.sumScore = dataExt.extrairGols(textoBase)
                elif('resultado correto - intervalo' in dado):
                    vencedorPrimeiroTempo = dataExt.extrairVencedorPrimeiroTempo(textoBase)
                    adversary1, adversary2 = dataExt.extrairAdversarios(partida.title)
                    idWinner = self.retornaDadosAdversarioPorNome(vencedorPrimeiroTempo, idCompetition)
                    idAdversary1 = self.retornaDadosAdversarioPorNome(adversary1, idCompetition)
                    idAdversary2 = self.retornaDadosAdversarioPorNome(adversary2, idCompetition)
                    halfTimeResult = dataExt.extrairResultadoPartida(textoBase)

                    if(None not in (idWinner, idAdversary1, idAdversary2, halfTimeResult)):
                        numGols1 = int(halfTimeResult.split('-')[0])
                        numGols2 = int(halfTimeResult.split('-')[-1])
                        maiorSaldoGols = numGols1 if numGols1 > numGols2 else numGols2
                        menorSaldoGols = numGols2 if numGols1 > numGols2 else numGols1
                        
                        if(idWinner == idAdversary1):
                            partida.halfTimeResult = f'{maiorSaldoGols}-{menorSaldoGols}'
                        elif(idWinner == idAdversary2):
                            partida.halfTimeResult = f'{menorSaldoGols}-{maiorSaldoGols}'
                        else:
                            partida.halfTimeResult = halfTimeResult
                elif('time a marcar primeiro' in dado):
                    scoreFirstAdvName = dataExt.extrairTimeMarcaPrimeiro(textoBase)
                    if(scoreFirstAdvName is not None and scoreFirstAdvName != ''):
                        partida.idAdversaryScoreFirst = self.retornaDadosAdversarioPorNome(scoreFirstAdvName, idCompetition)

            #CAPTURA IDs TIMES
            dicionarioNomesTimes = []
            if(len(matchMarkets) > 0 and winner != ''
            and adversary1 != '' and adversary2 != ''):
                partida.idWinner = self.retornaDadosAdversarioPorNome(winner, idCompetition)
                partida.idAdversary1 = self.retornaDadosAdversarioPorNome(adversary1, idCompetition)
                partida.idAdversary2 = self.retornaDadosAdversarioPorNome(adversary2, idCompetition)
                
                numGols1 = int(matchResult.split('-')[0])
                numGols2 = int(matchResult.split('-')[-1])
                maiorSaldoGols = numGols1 if numGols1 > numGols2 else numGols2
                menorSaldoGols = numGols2 if numGols1 > numGols2 else numGols1
                
                if(partida.idWinner == partida.idAdversary1):
                    partida.matchResult = f'{maiorSaldoGols}-{menorSaldoGols}'
                elif(partida.idWinner == partida.idAdversary2):
                    partida.matchResult = f'{menorSaldoGols}-{maiorSaldoGols}'
                else:
                    partida.matchResult = matchResult

                dicionarioNomesTimes = {'winner':winner, 'adversary1':adversary1, 'adversary2':adversary2}

            return partida, partidaRaw, dicionarioNomesTimes
        except Exception as ex:
            self.logger.error(f'Dados da partida(idFixture:{idFixture}) com problemas. Detalhes: {ex}')
            return None

    def calculaMaximas(self, jsonRawText, idCompetition, 
                        matchResultFinal, matchResultIntervalo,
                        idAdversary1, idAdversary2, idAdversaryScoreFirst):
        try:
            self.logger.info('Processando as maximas...')
            listaMaxTime = []
            #CALCULO MERCADO TIME MARCA PRIMEIRO
            listaMaxTime.append({'label':'casa marca primeiro sim', 'saiu': idAdversary1 == idAdversaryScoreFirst})
            listaMaxTime.append({'label':'casa marca primeiro nao', 'saiu': not (idAdversary1 == idAdversaryScoreFirst)})

            #CALCULO MERCADO MANDANTE HT/FT E EMPATE
            golCasaHT = int(matchResultFinal.split('-')[0])
            golVisitanteHT = int(matchResultFinal.split('-')[1])
            golCasaFT = int(matchResultFinal.split('-')[0])
            golVisitanteFT = int(matchResultFinal.split('-')[1])

            listaMaxTime.append({'label':'mandante HT', 'saiu': golCasaHT > golVisitanteHT})
            listaMaxTime.append({'label':'empate HT', 'saiu': golCasaHT == golVisitanteHT})
            listaMaxTime.append({'label':'visitante HT', 'saiu': golCasaHT < golVisitanteHT})
            listaMaxTime.append({'label':'mandante FT', 'saiu': golCasaFT > golVisitanteFT})
            listaMaxTime.append({'label':'empate FT', 'saiu': golCasaFT == golVisitanteFT})
            listaMaxTime.append({'label':'visitante FT', 'saiu': golCasaFT < golVisitanteFT})

            #CALCULO MERCADO HOME MARCA E AWAY MARCA
            golCasa = int(matchResultFinal.split('-')[0])
            golVisitante = int(matchResultFinal.split('-')[1])
            timeCasaMarca = golCasa > 0
            timeVisitanteMarca = golVisitante > 0
            listaMaxTime.append({'label':'casa marca sim', 'saiu': timeCasaMarca})
            listaMaxTime.append({'label':'casa marca nao', 'saiu': not timeCasaMarca})
            listaMaxTime.append({'label':'visitante marca sim', 'saiu': timeVisitanteMarca})
            listaMaxTime.append({'label':'visitante marca nao', 'saiu': not timeVisitanteMarca})
            
            #RESULTADO_FT
            typeMarkProvider = TypeMarketProvider()
            listaTypesResultado = typeMarkProvider.retornaTodosPorMercado(3)
            for typeMarket in listaTypesResultado:
                if(matchResultFinal in typeMarket.label):
                    listaMaxTime.append({'label':typeMarket.label, 'saiu': True})
                else:
                    listaMaxTime.append({'label':typeMarket.label, 'saiu': False})
               
            #RESULTADO_HT
            respEspecifico = False
            typeMarkProvider = TypeMarketProvider()
            listaTypesResultado = typeMarkProvider.retornaTodosPorMercado(5)
            for typeMarket in listaTypesResultado:
                if(typeMarket.idTypeMarket == 37):
                    continue
                if(matchResultIntervalo in typeMarket.label):
                    listaMaxTime.append({'label':typeMarket.label, 'saiu': True})
                    respEspecifico = True
                else:
                    listaMaxTime.append({'label':typeMarket.label, 'saiu': False})
            listaMaxTime.append({'label':'outro HT', 'saiu': not respEspecifico})

            for itemMaximaBase in listaMaxTime:                
                self.registraMaxima(idCompetition, itemMaximaBase, itemMaximaBase["label"])
                        
            #OUTROS MERCADOS
            matchMarkets = ast.literal_eval(jsonRawText)
            for dado in matchMarkets:
                listaTextoBaseSecoes = []
                dado = dado.strip().lower().replace(' ', '')
                listaTextoBaseSecoes = dataExt.extrairListaApostas(dado)
                if(len(listaTextoBaseSecoes) == 0):
                    continue

                labelBase = listaTextoBaseSecoes[0]['label']
                for itemMaximaBase in listaTextoBaseSecoes[1:]:
                    textoBuscaMarket = None
                    if('totaldegols' in labelBase):
                        tipo, valor = dataExt.extrairOverUnder(itemMaximaBase['label'].lower())
                        self.logger.info(f'ExtrairOverUnder -> Tipo: {tipo} -- Valor:{valor}')
                        if(tipo is None):
                            self.logger.info('Extracao do tipo/valor falhou.')
                            continue
                        else:
                            textoBuscaMarket = f'{tipo} {valor}'
                    elif('númerodegols' in labelBase):
                        valor = dataExt.extrairGolsExatos(itemMaximaBase['label'].lower())
                        textoBuscaMarket = f'gol {valor}'
                    elif('paraambosostimesmarcarem' in labelBase and 'resultado' not in labelBase):
                        tipo = 'sim' if 'yes' in itemMaximaBase['label'].lower() else 'nao'
                        textoBuscaMarket = f'ambas {tipo}'       
                    else:
                        continue
                    
                    sucesso = self.registraMaxima(idCompetition, itemMaximaBase, textoBuscaMarket)
                    if(not sucesso):
                        continue
        except Exception as ex:
            self.logger.error(f'Falha ao processar as maximas - Detalhe: {ex}')
    
    def registraMaxima(self, idCompetition, itemMaximaBase, textoBuscaMarket):
        maximaProv = MaximaProvider()
        typeMarkProvider = TypeMarketProvider()
        if(textoBuscaMarket is None):
            self.logger.info('Extracao do textoBuscaMarket falhou.')
            return False
        #BUSCA TYPE_MARKET PELO TITULO
        typeMarket = typeMarkProvider.retornaMarketPorLabel(textoBuscaMarket)
        if(typeMarket is None):
            self.logger.info(f'TypeMarket com label {itemMaximaBase["label"]} nao encontrado.')
            return False
        
        #BUSCA MAXIMA PELO idTypeMarket
        saiu = itemMaximaBase['saiu']
        maximaEncontrada = maximaProv.retornaPorTypeMarket(idCompetition, typeMarket.idTypeMarket, None)
        if(maximaEncontrada is not None):                        
            self.logger.info('Maxima encontrada.') 
            if(saiu):
                self.logger.info('Maxima rompida.')
                #ATUALIZA O CAMPO BROKEN DA ULTIMA DO BANCO E INSERE UMA NOVA COM lastSequenceCount = 0
                maximaEncontrada.broken = True
                maximaEncontrada.date = datetime.utcnow()
                maximaProv.atualizar(maximaEncontrada) 
                self.logger.info('Maxima atualizada para broken=True.') 
                maximaProv.inserir(self.gerarEntidadeMaxima(idCompetition, typeMarket.idTypeMarket, False))  
                self.logger.info('Nova maxima criada com ZERO a partir da rompida.')  
                return True 
            else:
                self.logger.info('Maxima nao foi rompida.')
                #APENAS ATUALIZA O lastSequenceCount DA ULTIMA DO BANCO
                maximaEncontrada.date = datetime.utcnow()
                maximaEncontrada.idCompetition = idCompetition
                maximaEncontrada.lastSequenceCount = maximaEncontrada.lastSequenceCount + 1
                maximaProv.atualizar(maximaEncontrada) 
                self.logger.info('Contador da maxima incrementado.')     
                return True
        else:
            self.logger.info('Maxima nao encontrada.')
            maxima = Maxima()
            maxima.date = datetime.utcnow()
            maxima.idCompetition = idCompetition
            maxima.idTypeMarket = typeMarket.idTypeMarket
            maximaProv.inserir(maxima)
            self.logger.info('Novo registro de Maxima criado.')
            return True

    def gerarEntidadeMaxima(self, idCompetition, idType, broken=None, lastSequence=None):
        maxima = Maxima()   
        if(broken is not None):
            maxima.broken = broken
        if(lastSequence is not None):
            maxima.lastSequenceCount = lastSequence
        maxima.idTypeMarket = idType
        maxima.date = datetime.utcnow()
        maxima.idCompetition = idCompetition
        return maxima

    def retornaFixtures(self, url):
        result = []
        listaJson = self.carregaJsonTela(url)
        for itemJson in listaJson['fixtures']:
            try:
                fixture = Fixture()
                fixture.idFixture = util.getAtributo(itemJson, 'fixtureId')
                fixture.description = util.getAtributo(itemJson, 'desc')            
                fixture.idCompetition = util.getAtributo(itemJson, 'competitionId')            
                fixture.idChallenge = util.getAtributo(itemJson, 'challengeId')            
                fixture.dateDescription = util.getAtributo(itemJson, 'dateDesc')
                time = util.getAtributo(itemJson, 'time')            
                fixture.time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S')
                result.append(fixture)
            except Exception as ex:
                self.logger.info(f'Falha ao captura os dados da fixture({fixture.idFixture}). Detalhes: {ex}')
        self.logger.info('JSON fixtures carregado.')
        return result

    def montarUrlFixture(self, competitionId, dataInicio, dataFim):
        sportId = cfgEspecifico.configParams['DATA_SPORT_ID']
        sportDescriptor = cfgEspecifico.configParams['DATA_SPORT_DESCRIPTOR']
        challengeId = '0'
        fixtureId = '0'
        isDynamic = 'False'
        linkId = '0'
        teamId = '0'        
        return cfgEspecifico.urls['URL_JSON_BASE_FIXTURE'].format(sportId, competitionId, challengeId, 
                                                            fixtureId, dataInicio, dataFim, isDynamic, 
                                                            linkId, teamId, sportDescriptor)

    def montarUrlResultadoPartida(self, competitionId, dataInicio, dataFim, fixtureId, challengeId):
        sportId = cfgEspecifico.configParams['DATA_SPORT_ID']
        return cfgEspecifico.urls['URL_JSON_BASE_PARTIDA'].format(sportId, fixtureId, competitionId,\
            dataInicio, dataFim, challengeId)

    def carregaSessao(self):
        while self.sessionCookie is None\
        or self.sessionCookie.endswith('000003'):  
            self.sessionCookie = self.getCookie(self.browserSession.get_cookies(), '.bet365.com', 'pstk')
            self.GetRequest(cfgEspecifico.login_credenciais['URL_LOGIN'])
            self.logger.info(f'COOKIE SESSAO: {self.sessionCookie}')
            time.sleep(5)

    def GetFastRequestJson(self, url):
        try:
            cookieGerado = cfgPadrao.cookie['SESSION_COOKIE'].format(self.sessionCookie)
            headers = {
                'Cookie': cookieGerado,
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
            }
            r = requests.get(url, headers=headers)
            return r.json(), r.status_code            
        except KeyError:
            return None, 500

    def carregaJsonTela(self, url):
        try:
            dados = None
            statusCode = 401       
            if(self.sessionCookie is None):
                self.logger.info(f'Detectada primeira requests, carregando cookie de sessao...')  
                self.carregaSessao()      

            while statusCode == 401:
                self.logger.info(f'Acessando URL json...{url}')            
                jsonText, statusCode = self.GetFastRequestJson(url)
                if(statusCode == 401):
                    self.logger.info('Carregamento do JSON não autorizado. Verificar login.')
                    self.efetuaLogin()
                    self.carregaSessao()
                    dados = None
                else:
                    self.logger.info(f'Carregamento do JSON autorizado..')
                    dados = jsonText
                    statusCode = 200
            return dados
        except Exception as jex:
            self.logger.error(f'Falha ao retornar JSON: {jex}')        
            if('line 1 column 1' in str(jex).lower()):
                self.efetuaLogin()
                self.carregaSessao()

    def extrairApostaVencedora(self, texto):
        for secao in texto.split('|'):
            if 'won' in secao.lower():
                return secao
        return 'N/A'

    def extrairListaHeader(self, colunas):
        resp = []
        for coluna in colunas:
            resp.append(coluna.text)
        return resp

    def retornaDadosAdversarioPorNome(self, nome, idCompetition):
        if(nome is None or nome == ''):
            return None
        for item in self.listaAdversarys:
            if(nome.lower().strip() == item.name.lower().strip()\
            and idCompetition == item.idCompetition):
                return item.idAdversary
        #SE NAO EXISTIR, GRAVA UM NOVO E RETORNA O ID
        adsProv = AdversaryProvider()
        newAd = Adversary()
        newAd.name = nome
        newAd.idCompetition = idCompetition
        idNovo = adsProv.atualizar(newAd)
        self.listaAdversarys = adsProv.retornaTodos()
        return idNovo
        
    def sleep(self, tempo=None):
        if(tempo is None):
            tempo = self.limitadorTempo
        self.logger.info(f'Aguardando {tempo} segundos...')
        time.sleep(tempo)




