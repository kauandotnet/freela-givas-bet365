import re
from business.extrator import extrairGols, extrairResultadoPartida, extrairVencedor

def test_gols():
    inputData = '0 goals~won~'
    expected = '0'
    assert extrairGols(inputData) == expected, "Deveria ser 0"

def test_vencedor_empate():
    inputData = 'draw~won~'
    expected = 'draw'
    assert extrairVencedor(inputData) == expected, "Deveria ser draw"

def test_vencedor_unico():
    inputData = 'frança~won~'
    expected = 'frança'
    assert extrairVencedor(inputData) == expected, "Deveria ser frança"

def test_resultado_empate():
    inputData = 'draw #0-0~won~'
    expected = '0-0'
    assert extrairResultadoPartida(inputData) == expected, "Deveria ser 0-0"
    
def test_resultado_com_vencedor():
    inputData = '=EUA #1-0~Won~' #'argentina #1-0~won~'
    expected = '1-0'
    assert extrairResultadoPartida(inputData) == expected, "Deveria ser 1-0"    