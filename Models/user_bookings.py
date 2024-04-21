from sqlmodel import SQLModel, Field

class Bookings(SQLModel, table=True):
    id:int = Field(default= None, primary_key= True)
    customer_name: str
    pickup_date: str
    delivery_date: str
    gender:str
    status:str= Field(description=["pending","completed","cancelled"])
    total_amount: float

class Item(SQLModel):
    name: str
    description: str
    price: float
    quantity:int
    instruction:str

