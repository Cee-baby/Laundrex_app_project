from datetime import datetime, timedelta
from typing import Annotated,Any,Optional
from fastapi import FastAPI,Depends,HTTPException,status
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import SQLModel, Field,Column,VARCHAR
from pydantic import field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber




def datetime_now_sec():
    return datetime.now().replace(microsecond=0)


class UserLogin(SQLModel):
    email: str=Field(description="Email of the User")
    password:str=Field(min_length=8,max_length=100,description="Password of the User",title="Password")

class UserCreate(SQLModel):
    full_name: str = Field(default="",min_length=3,max_length=50,description="full_name of the User")
    email: str=Field(unique=True,index=True,description="Email of the User")
    password: str = Field(min_length=8, max_length=100, description="Password of the User",title="Password") 
    # phone: PhoneNumber = Field(description="Phone number of the passenger", title="Phone Number", schema_extra={})

   
    

class User(UserCreate,table=True):
    id: int = Field(default=None,unique=True,primary_key=True)
    created: datetime = Field(default_factory=datetime_now_sec)
    modified: datetime = Field(default_factory=datetime_now_sec)
    is_active: bool = Field(default=False)
    is_superuser: bool = Field(default=False,description="Is for admin users",title="Is Super User")
    


class Token(SQLModel):
    access_token: str
    token_type : str="bearer"

class TokenData(SQLModel):
    sub: int | None = None

class UserOutput(SQLModel):
    id: int
    name: str
    email: str
    phone: PhoneNumber


class Message(SQLModel):
    message: str


class NewPassword(SQLModel):
    token: str
    new_password: str