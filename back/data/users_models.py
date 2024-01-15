from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from pydantic import constr, BaseModel, Field


EMAIL = constr(pattern='([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
Base = declarative_base()


class Users(Base):
    __tablename__ = 'Users'
    user_id = Column(String(255), primary_key=True)
    email = Column(String(50))
    first_name = Column(String(50))
    last_name = Column(String(50))
    password = Column(String(255))
    auth_code = Column(String(255))
    is_verified = Column(Integer())
    

class RegistrationData(BaseModel):
    email: EMAIL = Field(min_length=8, max_length=50)
    password: str = Field(min_length=8, max_length=255)
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)


class LoginData(BaseModel):
    email: str = Field(min_length=4, max_length=50)
    password: str = Field(min_length=8, max_length=255)