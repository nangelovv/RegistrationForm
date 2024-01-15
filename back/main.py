from routers.users_routers import UsersRouters
from data.users_models import Users, Base
from common.common_params import engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from common.secret import *
import logging, os


Base.metadata.create_all(bind = engine, tables = [
    Users.__table__,
])

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"],
    allow_credentials = True
)

users = UsersRouters()

os.environ['API_KEY'] = API_KEY
os.environ['EMAIL_KEY'] = EMAIL_KEY

app.include_router(users.router)