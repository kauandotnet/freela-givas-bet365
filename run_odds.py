import os
import sys
from crawlers.bet365virtualOdds import CrawlerBet365VirtualOdds

try:
    erro = False
    CrawlerBet365VirtualOdds(True)
except Exception as ex:
    print('Ocorreu um erro ao tentar rodar os crawlers. Detalhe:' + str(ex))
    erro = True
