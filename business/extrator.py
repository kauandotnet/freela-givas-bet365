import re

def extrairApostaVencedora(texto):
    for secao in texto.split('|'):
        if 'won' in secao.lower():
            return secao
    return 'N/A'

def extrairApostaVencedoraComGols(texto):
    for secao in texto.split('|'):
        if 'won' in secao.lower() and 'goal' in secao.lower():
            return extrairVencedor(secao)
    return 'N/A'

def extrairGolsExatos(texto):
    m = re.search(r'(\d\s*)', texto)
    if(m):
        return m.group(1).replace(' ','').strip()
    return None

def extrairVencedor(texto):
    return texto.replace('~won~','').replace('=','').capitalize().strip()

def extrairListaApostas(texto):
    result = []
    for secao in texto.split('|'):
        result.append({'label':secao, 'saiu': 'won' in secao.lower()}) 
    return result

def extrairVencedorPrimeiroTempo(texto):
    base = texto.replace('~won~','').replace('=','')
    if('#' in base):
        return base.split('#')[0].capitalize().strip()
    else:
        return None

def extrairTimeMarcaPrimeiro(texto):
    try:
        if('no team' not in texto.lower()):
            return texto.lower().replace('to score first~won~','').replace('=','').capitalize().strip()
        else:
            return None
    except:
        return None
        
def extrairGols(texto):
    m = re.search(r'(\d)', texto)
    if(m):
        return m.group(1).replace(' ','').strip()
    return None

def extrairResultadoPartida(texto):
    m = re.search(r'(\d\s*-\s*\d)', texto)
    if(m):
        return m.group(1).replace(' ','').strip()
    return None

def extrairAdversarios(texto):
    m = re.search(r'(?i)(\d.\d*)\s*(\w.*)\s* v \s*(\w.*)', texto)
    if(m):
        return m.group(2).strip(), m.group(3).strip()

    return None, None

def extrairPosicaoFinalSpeedway(texto, nameAdversary):
    listaNomes = texto.split('|')
    for index, item in enumerate(listaNomes):
        if(nameAdversary.lower() in item.lower()):
            return index
    return None

def extrairOverUnder(texto):
    valorLimite = None
    vencedor = extrairVencedor(texto)
    m = re.search(r'(\d\s*.\s*\d)', texto)
    if(m):
        valorLimite = m.group(1).replace(' ','').strip()

    if('over' in vencedor.lower()):
        return 'over', valorLimite
    elif('under' in vencedor.lower()):
        return 'under', valorLimite
    
    return None, valorLimite
    