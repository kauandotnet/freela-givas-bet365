import re

def extrairVencedor(texto):
    return texto.replace('~won~','').replace('=','').capitalize().strip()

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
    if(texto == '' or texto is None):
        return None
    m = re.search(r'(\d)', texto)
    if(m):
        grupo = m.group(1)
        return grupo.replace(' ','').strip() if grupo is not None else None
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
