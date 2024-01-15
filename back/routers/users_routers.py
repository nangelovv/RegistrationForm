from fastapi import APIRouter, Depends, Request, File
from common.common_params import CommonParams, session
from common.responses import BadRequest
from data.users_models import *
from services import users_services
from typing import Annotated
import json


class UsersRouters:
    def __init__(self: 'UsersRouters'):
        self.router = APIRouter(prefix = '/users')
        self.router.add_api_route("/", self.login, methods = ["POST"])
        self.router.add_api_route("/register", self.register, methods = ["POST"])
        self.router.add_api_route("/email", self.change_email, methods = ["POST"])
        self.router.add_api_route("/password", self.change_password, methods = ["POST"])
        self.router.add_api_route("/verify", self.verify, methods = ["POST"])
        self.router.add_api_route("/", self.delete, methods = ["DELETE"])

    def login(self: 'UsersRouters', data: LoginData):
        user = users_services.try_login(data.email , data.password, session())
        if user:
            token = users_services.create_token(user)
            data = {
                "token": token,
                "user_id": user.user_id,
                "email": user.email,
                "is_verified": user.is_verified,
                }
            return json.dumps(data)
        else:
            return BadRequest('Invalid login data.')

    def register(self: 'UsersRouters', data: RegistrationData):
        return users_services.register(data, session())
    
    async def change_email(self: 'UsersRouters', request: Request, commons: Annotated[CommonParams, Depends()]):
        data = await request.json()
        return users_services.change_email(data["txt"], token = commons.token, session = commons.session)
    
    async def change_password(self: 'UsersRouters', request: Request, commons: Annotated[CommonParams, Depends()]):
        data = await request.json()
        return users_services.change_password(data["txt"], token = commons.token, session = commons.session)
    
    async def verify(self: 'UsersRouters', request: Request, commons: Annotated[CommonParams, Depends()]):
        data = await request.json()
        return users_services.verify(data["txt"], token = commons.token, session = commons.session)

    async def delete(self: 'UsersRouters', commons: Annotated[CommonParams, Depends()]):
        return users_services.delete(token = commons.token, session = commons.session)