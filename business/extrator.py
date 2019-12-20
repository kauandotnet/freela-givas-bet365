import re

def extrairVencedor(texto):
    return texto.replace('~won~','').replace('=','').capitalize().strip()

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
    m = re.search(r'(?i)(\d.\d*)\s*(\w.*)\s*v\s*(\w.*)', texto)
    if(m):
        return m.group(2).strip(), m.group(3).strip()

    return None, None
