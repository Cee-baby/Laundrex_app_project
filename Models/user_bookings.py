from typing import List
from pydantic import BaseModel,Field

class Cloth(BaseModel):
    cloth_id: str
    quantity: int

class Bookings(BaseModel):
    id:int = Field(default= None, primary_key= True)
    

class BookingsCreate( BaseModel):
    customer_name: str = Field(...)
    pickup_date: str = Field(...)
    delivery_date: str = Field(...)
    gender:str = Field(...)
    status:str= Field(description="")
    quantity:int 
    price:float
    instruction:str
    total_amount: int=Field(...,description="Total amount",ge= 0)
    cloth:Cloth
    bookings:Bookings
    

# class Item(BaseModel):
#     name: str
#     description: str
#     price: float
#     quantity:int
#     instruction:str

