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

class Crawler(object):
    
    def __init__(self):
        self.dominio = ''
        self.urlDominio = ''
        self.browserSession = None
        
    def GetRequest(self, url):
        return self.browserSession.get(url)

    def GetRequestWithAgent(self, url):
        if(self.browserSession is None):
            headers = {'User-Agent': cfgPadrao.configParams['USER_AGENT'] }
            if(headers is not None):
                return requests.get(url, headers=headers)
            else:
                return requests.get(url)
        else:
            return self.browserSession.get(url)

    def GetRequestString(self, url):
        getResult = self.browserSession.get(url)
        return lxml.html.fromstring(getResult.content)

    def GetRequestStringEncoded(self, url, encode):
        getResult = self.browserSession.get(url)
        getResult.encoding = encode
        return lxml.html.fromstring(getResult.content)        

    def GetElementObject(self, driver, xpath):
        obj = None
        try:
            obj = driver.xpath(xpath)
        except Exception:
            obj = None
        return obj

    def GetQueryElementObject(self, driver, xpath):
        obj = None
        try:
            obj = driver.xpath(xpath)
        except Exception:
            obj = None
        return obj

    def getCookie(self, cookiesList, domain, name):
        for cookie in cookiesList:
            if (cookie['domain'].strip() == domain.strip()
            and cookie['name'].strip() == name.strip()): 
                return cookie['value'].strip()
        return None

    def RetornaLinksPaginas(self, xpathBar, html):
        listLinks = []
        for item in html.xpath(xpathBar):
            if(str.isdigit(item.text)):
                listLinks.append(item.get('href'))
        return listLinks
        
