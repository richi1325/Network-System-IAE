import os
from sqlalchemy import create_engine

def create_connection():
    return create_engine(f'postgresql+psycopg2://{os.environ["POSTGRES_USER"]}:{os.environ["POSTGRES_PASSWORD"]}@{os.environ["HOST"]}/{os.environ["POSTGRES_DB"]}').connect()