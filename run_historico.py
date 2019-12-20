import os
import sys
import config as cfgPadrao
from crawlers.bet365virtual import CrawlerBet365Virtual

try:
    erro = False
    CrawlerBet365Virtual(True)
except Exception as ex:
    print('Ocorreu um erro ao tentar rodar os crawlers. Detalhe:' + str(ex))
    erro = True
