import re
from business.extrator import extrairGols, extrairTimeMarcaPrimeiro,\
                                extrairResultadoPartida, extrairVencedor,\
                                extrairVencedorPrimeiroTempo, extrairApostaVencedoraComGols

def test_gols():
    inputData = '0 goals~won~'
    expected = '0'
    assert extrairGols(inputData) == expected, "Deveria ser 0"

def test_vencedor_empate():
    inputData = 'draw~won~'
    expected = 'Draw'
    assert extrairVencedor(inputData) == expected, "Deveria ser Draw"

def test_vencedor_unico():
    inputData = 'frança~won~'
    expected = 'França'
    assert extrairVencedor(inputData) == expected, "Deveria ser frança"

def test_resultado_empate():
    inputData = 'draw #0-0~won~'
    expected = '0-0'
    assert extrairResultadoPartida(inputData) == expected, "Deveria ser 0-0"
    
def test_resultado_com_vencedor():
    inputData = '=EUA #1-0~Won~' #'argentina #1-0~won~'
    expected = '1-0'
    assert extrairResultadoPartida(inputData) == expected, "Deveria ser 1-0"    

def test_resultado_intervalo_com_vencedor():
    inputData = '=Japão #1-0~Won~'
    expected = '1-0'
    assert extrairResultadoPartida(inputData) == expected, "Deveria ser 1-0"    

def test_time_marca_primeiro():
    inputData = '=Japão to score first~Won~'
    expected = 'Japão'
    assert extrairTimeMarcaPrimeiro(inputData) == expected, "Deveria ser Japão"    

def test_time_vencedor_primeiro():
    inputData = '=Japão #1-0~Won~'
    expected = 'Japão'
    assert extrairVencedorPrimeiroTempo(inputData) == expected, "Deveria ser Japão"    

def test_time_vencedor_primeiro_empate():
    inputData = '=draw #1-1~won~'
    expected = 'Draw'
    assert extrairVencedorPrimeiroTempo(inputData) == expected, "Deveria ser Japão"    

def test_time_gols_exatos():
    inputData = '0goals~~'
    expected = '0'
    assert extrairApostaVencedoraComGols(inputData) == expected, "Deveria ser 0"    

    