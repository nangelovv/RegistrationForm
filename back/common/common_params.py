from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Security
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .secret import sql_database


engine = create_engine(sql_database)
session = sessionmaker(bind = engine)


class CommonParams:
    def __init__(self, head_token: HTTPAuthorizationCredentials = Security(HTTPBearer())):
        self.head_token = head_token
        self.token = head_token.credentials
        self.session = session()