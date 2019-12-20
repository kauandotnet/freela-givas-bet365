import csv
import os
import time
import urllib.request
from enum import Enum
from pathlib import Path
from socket import timeout
from urllib.request import urlopen

import dashtable
import lxml
import requests
import xlsxwriter
from bs4 import BeautifulSoup

import util
import config as cfgPadrao
from crawlers.baseCrawler import Crawler
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class CrawlerSelenium(Crawler):
    
    def __init__(self):
        self.dominio = ''
        self.urlDominio = ''
        self.browserSession = None
        self.logger = None
        self.listaErros = []
        self.contScreens = 1
        self.saveRequestImage = False

    def GetRequest(self, url, useSelenium=True):
        if(not useSelenium):
            return super().GetRequest(url)

        if(self.saveRequestImage):
            self.browserSession.save_screenshot(f"data/screens/screen_{self.contScreens}.png")
            self.contScreens += 1
        if(self.browserSession.current_url == url):
            return

        trys = 0
        sucesso = False
        while(trys <= 4):
            try:
                urlAtual = 'http://www.comercialgomes.com.br/home/'
                while(urlAtual == 'http://www.comercialgomes.com.br/home/'):
                    if(self.browserSession is not None):
                        self.browserSession.get(url)
                        urlAtual = self.browserSession.current_url
                        self.logger.info('INFO --> Aguardando carregamento da página...')
                    else:
                        return None   

                if(url in self.listaErros):                    
                    self.listaErros.remove(url)

                sucesso = True
                break
            except TimeoutException:
                print('ERRO --> Timeout ao tentar carregar o produto, tentando novamente em 5s...')
                time.sleep(2)
                trys += 1
        
        if(url not in self.listaErros and not sucesso):
            self.listaErros.append(url)

    def GetRequestJson(self, url):
        self.GetRequest(url)
        objAuth = self.GetElementObject('//div[@id="content"]//h2')
        if(objAuth):
            return 'Não autorizado', 401
        elem = self.browserSession.find_element_by_tag_name("body")
        if(elem):
            return elem.text, 200
        return None, 500

    def GetAllElementObject(self, xpathName, alternativeXpath=None):
        browser = self.browserSession
        obj = None
        try:
            browser.implicitly_wait(2)
            obj = browser.find_elements_by_xpath(xpathName)
        except Exception:
            obj = None        

        if(not obj and alternativeXpath is not None):
            try:
                obj = browser.find_elements_by_xpath(alternativeXpath)
            except Exception:
                obj = None     

        return obj

    def GetQueryElementObject(self, xpathName, timeout=15):
        browser = self.browserSession
        obj = None
        try:
            obj = WebDriverWait(browser, timeout).until(EC.presence_of_element_located((By.XPATH, xpathName)))
        except Exception:
            obj = None        

        return obj

    def GetChildElementObject(self, parent, xpathName):
        browser = self.browserSession
        obj = None
        try:
            browser.implicitly_wait(2)
            obj = parent.find_element_by_xpath(xpathName)
        except Exception:
            obj = None        

        return obj

    def GetAllChildElementObject(self, parent, xpathName):
        browser = self.browserSession
        obj = None
        try:
            obj = parent.find_elements_by_xpath(xpathName)
        except Exception:
            obj = None        

        return obj

    def GetElementObject(self, xpathName, widgetCheck=True):
        browser = self.browserSession
        obj = None
        try:
            obj = WebDriverWait(browser, 8).until(EC.presence_of_element_located((By.XPATH, xpathName)))
        except Exception:
            obj = None        
        
        if(obj is None):
            try:
                obj = WebDriverWait(browser, 8).until(EC.presence_of_element_located((By.XPATH, cfg.altProductXPaths['ALT_' + xpathName])))
            except Exception:
                obj = None   
        return obj

    def getTextoElemento(self, elemento):
        try:
            return elemento.text.strip()
        except:
            return ''

    def getAtributoElemento(self, elemento, atributoNome):
        try:
            return elemento.attr(atributoNome).strip()
        except:
            return ''

    def GetElementValue(self, element, configXPathName):
        if('ATT_' in configXPathName):
            if('HREF' in configXPathName):
                return element.get_attribute('href').strip()
        elif('TXT' in configXPathName):
            return element.text.strip()
        elif('HTM' in configXPathName):
            return util.ModelarDescricao(util.CleanHtml(util.stringify_children(element)))

    def scrollElementIntoView(self, element, yoffset):
        y = element.location['y'] - yoffset
        self.browserSession.execute_script('window.scrollTo(0, {0})'.format(y))
        
    def close(self):
        self.browserSession.close()
