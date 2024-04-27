from fastapi import APIRouter,Depends,HTTPException, Query
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from Deps.deps import get_db,get_current_user
from Models.contact import (
    ContactUs
)
from typing import Annotated, List
from fastapi.encoders import jsonable_encoder
from Models.user_models import User


contact_router = APIRouter(tags=["Contact_Us"])

@contact_router.post("/contact-us/services")
async def contact_us(contact_us: ContactUs, current_user: Annotated[User, Depends(get_current_user)], db: Annotated[Session,Depends(get_db)]):
    print("Received contact request from {contact.full_name}<{contact.email}>")
    print(f"Subject:{contact_us.subject}")
    print(f"Message:{contact_us.message}")
    return {"message": "Contact request submitted successfully"}