from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import config as cfg

engine = create_engine(cfg.database['mysql_conn_prod'])
Session = sessionmaker(bind=engine)
Base = declarative_base()

