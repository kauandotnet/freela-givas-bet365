from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from business.base import Base
from business.maxima import Maxima
from business.fixture import Fixture
from business.adversary import Adversary
from business.matchdata import MatchData
from business.matchodds import MatchOdds
from business.typemarket import TypeMarket
from business.competition import Competition
from business.matchdataraw import MatchDataRaw
import config as cfg

engine = create_engine(cfg.conexao_banco_ativa['mysql_conn'])
Base.metadata.create_all(engine)