from sqlmodel import SQLModel, Field, Column, ARRAY, JSON
from typing import List,Optional



class Cloth(SQLModel):
    cloth_name: str
    quantity: int
    category: str=Field(...,description="Men,Women,Others")




class BookingsCreate(SQLModel):
    user_name: str = Field(...,)
    phonenumber:str
    pickup_date: str = Field(...,)
    address: str=Field(...,min_length=1,max_length=100)
    instruction:Optional[str] = Field(...,min_length=0, max_length=100,)
    clothes: List[Cloth] = Field(sa_column=Column(JSON))
    booking_fulfilled: bool = Field(default=False)
    total_price: float=Field(...,description="Total amount",ge= 0)
    total_quantity:int
    
    

    class Config:
        arbitrary_types_allowed = True


class Bookings(BookingsCreate, table=True):
    id:int = Field(default= None, primary_key= True)
    user_id: int = Field(..., description="User id")

    




