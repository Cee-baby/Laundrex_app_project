from datetime import datetime,timedelta
from typing import Annotated
from fastapi import FastAPI,Depends,HTTPException,status
from jose import JWTError, jwt
from sqlmodel import SQLModel,Field


    

class NewsCreate(SQLModel):
    title:str
    description:str
    image:str

class News(NewsCreate,table= True):
    id:int=Field(default=None,primary_key=True,unique=True)


