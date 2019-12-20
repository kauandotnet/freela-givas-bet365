import csv
import math
import os
import re
import time
import urllib.request
from itertools import chain
from os import listdir
from os.path import isfile, join
from pathlib import Path
from socket import timeout
from urllib.request import urlopen

import dashtable
import lxml
import requests
import xlsxwriter
from bs4 import BeautifulSoup
from ftfy import fix_encoding, fix_text, fix_text_encoding
from openpyxl import load_workbook

import config as cfgPadrao


def getAtributo(obj, nome):
    try:
        return obj[nome]
    except:
        return ''

def SaveStateFile(text, ext):    
    fullPath = './data/state' + ext
    with open(fullPath, mode="w" , encoding="utf-8") as myfile:
        myfile.write(text)

def LoadStateFile():
    try:
        fullPath = './data/state.txt'
        f = open(fullPath,'r')
        text = f.read()
        return text       
    finally:
        f.close()
        
def ExtractLinksFromElements(productElements):
    tempList = []
    for liItem in productElements:           
        href = liItem.find_element_by_class_name('vip').get_attribute('href')       
        if(href == ''):
            continue
        tempList.append(href)
    return tempList

def RemoveWords(query):
    stopwords = cfgPadrao.wordExcludeList
    resultwords  = [word for word in re.split("\W+",query) if word.lower() not in stopwords]
    return ' '.join(resultwords)

def ExtractValideText(query):  
    return RemoveWords(fix_encoding(query))

def ChangeUrlEstructure(url, old, new):
    return url.replace(old, new)

def AppendToUrl(baseUrl, parameter, paramValue):    
    if(parameter not in baseUrl):
        return baseUrl + '/{0}/{1}'.format(parameter, paramValue)
    else:
        return baseUrl

def ChangeURLParameter(baseUrl, parameter, paramValue):    
    if(parameter not in baseUrl):
        return baseUrl + '&{0}={1}'.format(parameter, paramValue)
    else:
        return baseUrl

def ChangeURLParameterSeparator(baseUrl, parameter, paramValue, separator):    
    if(parameter not in baseUrl):
        return baseUrl + '{2}{0}={1}'.format(parameter, paramValue,separator)
    else:
        return baseUrl

def RemoveAllUrlParameter(baseUrl):
    return baseUrl.split('?')[0]   

def ExtractNumber(text):
    expressao = cfgPadrao.configParams['PAR_FIND_NUMBER_EXP']
    numbers = re.findall(expressao, text)
    if(len(numbers) > 0):
        return numbers[0]
    else:
        return text

def ExtractNumbersCompiled(text):
    p = re.compile(r'\b\d{1,3}(?:\.\d{3})*,\d+\b')
    return re.findall(p, text)
    
def FixUrlPath(urlPath):
    return urlPath.replace(' ','%20')

def AdicionarQuebraLinhaExcel(texto):
    texto = texto.split('\LF')
    baseFormula = '=CONCATENAR({0})'
    params = ''
    for item in texto:
        params += '"' + item + '"' + ',CARACT(10),'
    return baseFormula.format(params[:-10])

def CleanHtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext.replace(u'\xa0', u' ')

def ModelarDescricao(descricaoHtml):
    noWrap = descricaoHtml.replace('</p><p>','\LF').replace('<br>','\LF').replace('\LF\LF','\LF')
    noWrap = noWrap.replace('\r','').replace('\n','').replace('\t','')
    noWrap = CleanHtml(noWrap).strip()
    return noWrap.replace('</spa','')

def stringify_children(node):
    if node is None or (len(node) == 0 and not getattr(node, 'text', None)):
        return ""
    node.attrib.clear()
    opening_tag = len(node.tag) + 2
    closing_tag = -(len(node.tag) + 3)
    finalHtml = lxml.html.tostring(node, encoding='unicode')[opening_tag:closing_tag]
    return fix_encoding(finalHtml)

def getindexdefault(lista, elem, default):
    try:
        thing_index = lista.index(elem)
        return thing_index
    except ValueError:
        return default

def PreencherLacunasCabecalho(rowText):
    tamanhoAtual = len(rowText.split(';'))
    tamanhoEsperado = int(cfgPadrao.configParams['HEADER_TOTAL_SIZE'])
    restante = (tamanhoEsperado-tamanhoAtual)

    for index in range(restante):
        rowText += ' ;'
    return rowText + ' ;'

def convertSentenceToCapital(sentence):
    result = ''
    for word in sentence.split(' '):
        if(len(word) > 1):
            result += word.capitalize() + ' '
        else:
            result += word + ' '
    return result.strip()

def convertStringToMonetary(valor):
    try:
        return float(valor.replace('.','').replace(',','.'))
    except Exception:
        return 0.0

def titleize(text):
    exceptions = []
    exceptions += cfgPadrao.termos_ligacao
    return ' '.join([word if word in exceptions else word.title() for word in text.split()])

def GellAllImageFiles():
    LOCAL_PATH = cfgPadrao.configPaths['CFG_IMAGE_FOLDER']
    onlyfiles = [f for f in listdir(LOCAL_PATH) if isfile(join(LOCAL_PATH, f))]
    return onlyfiles

    # ============================================================

def findPeso(text):    
    text = text.lower().replace('.',',')
    regex = ''
    regex = r'(\d*\,?\d+)\s*(quilos?|kg|g|G)'
    p = re.compile(regex)
    m = p.search(text)
    if (m):
        return m.group()
    return 'N/A'

def floatToStr(inpt):
    return str(inpt).replace('.',',')

def converterMetrosParaCentimetros(tupDim):
    return tuple([100 * x if x != 30 else x for x in tupDim])

def converterMilimetroParaCentimetros(tupDim):
    return tuple([10 * x if x != 30 else x for x in tupDim])

def converterDimensoes(tupDim, valorAdicional=0):
    result = []
    for dim in tupDim:
        if(type(dim) is str):
            num = float(dim.replace('.','').replace(',','.'))
            result.append(num + valorAdicional)
        else:
            result.append(dim + valorAdicional)
    return tuple(result)

def getNumDimensionsFound(text):
    if('comp' in text.strip().lower() and 'larg' in text.strip().lower()):
        return text.lower().split(')')[-1].count('x')
    else:
        return text.lower().split(':')[-1].count('x')
    
def extrairDimensoes(text, conversao=False, 
                    defaultNoneString='30', valorAdicional=0):  
    resultTup = defaultNoneString, defaultNoneString, defaultNoneString  
    text = text.lower().replace('.',',')
    regex = ''
    numDimensions = getNumDimensionsFound(text)
    if(numDimensions < 1):
        regex = r'(?i)(?P<l>\d+(\,\d+)?)\s*\w*'
        p = re.compile(regex)
        m = p.search(text)
        if (m):
            resultTup = m.group("l"), defaultNoneString, defaultNoneString
    elif(numDimensions == 1):
        regex = r'(?i)(?P<l>\d+(\,\d+)?)\s*\w*x\s*(?P<w>\d+(\,\d+)?)\s*'
        p = re.compile(regex)
        text = text.replace('l:','').replace('a:','').replace('c:','').replace(':','')
        m = p.search(text)
        if (m):
            resultTup = m.group("l"), m.group("w"), defaultNoneString
    elif(numDimensions == 2):
        regex = r'(?P<l>\d+(\,\d+)?)\s*x\s*(?P<w>\d+(\,\d+)?)\s*x\s*(?P<h>\d+(\,\d+)?)'
        p = re.compile(regex)
        text = text.replace('l:','').replace('a:','').replace('c:','').replace(':','')
        m = p.search(text)
        if (m):
            resultTup = m.group("l"), m.group("w"), m.group("h")

    if(not conversao):
        return resultTup
    else:
        return converterDimensoes(resultTup, valorAdicional)