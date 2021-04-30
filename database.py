from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import psql_credentials

DATABASE_URL = f'postgresql+psycopg2://{psql_credentials["user"]}:{psql_credentials["pass"]}@' \
               f'{psql_credentials["host"]}:{psql_credentials["port"]}/{psql_credentials["dbname"]}'

engine = create_engine(DATABASE_URL, echo=False)

SessionMaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionMaker()
    try:
        yield db
    finally:
        db.close()
