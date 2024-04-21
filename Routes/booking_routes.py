from fastapi import APIRouter,Depends,HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from Deps.deps import get_db
from Models.user_bookings import (
    Bookings

)
from Models.user_models import User

from Routes import crud
from datetime import timedelta

booking_router = APIRouter(tags=["Bookings"])


    
cloth_types = {
        "men":{
        "polo":"polo for men",
        "senator-wear":"senator-wear for men", 
        "T-shirt":"T-shirt for men","image_url": "https://images.pexels.com/photos/996329/pexels-photo-996329.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",

        "jean-trousers":"Jean-trousers for men", "image_url":"https://images.pexels.com/photos/7764611/pexels-photo-7764611.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
        
        },
        "women":{
            "blouse":"blouse for women",
            "leggins":"leggins for women",
            "skirt":"skirt is for women","image_url":"https://www.pexels.com/photo/woman-wearing-white-long-sleeved-shirt-and-blue-skirt-1007018/",
            "Gown":"Gown is for women","image_url": "https://images.pexels.com/photos/7137418/pexels-photo-7137418.jpeg?auto=compress&cs=tinysrgb&w=600"
        },
        "others":{
            "sweater":"This is categorized for others","image_url":"https://images.pexels.com/photos/1183266/pexels-photo-1183266.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            "jeans":"This is categorized for others", "image_url":"https://images.pexels.com/photos/7764611/pexels-photo-7764611.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            "bedcover":"This is categorized as others","image_url":"https://images.pexels.com/photos/1841149/pexels-photo-1841149.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            "singlet":"This is categorized as others","image_url":"https://images.pexels.com/photos/4980308/pexels-photo-4980308.jpeg?auto=compress&cs=tinysrgb&w=600",
            "towel":"This is categorized as others", "image_url":"https://images.pexels.com/photos/4210376/pexels-photo-4210376.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            
        },
    }
@booking_router.post("/book_cloth/{cloth_type_id}")
async def book_cloth(user_id:int,cloth_type_id: int, session:Session=Depends(get_db)):
    user = session.get(User,user_id)
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    if cloth_type_id not in cloth_types:
        raise HTTPException(status_code=404,detail="Cloth_type_id not found")
    booking=Bookings(user_id=user_id,cloth_type_id=cloth_type_id)
    session.add(booking)
    session.commit()

    cloth_type =cloth_types[cloth_type_id]
    return{"message":f"sucessfully booked {cloth_type['name']} for {user.name}"}

@booking_router.get("/user-bookings/{user_id}")
async def get_user_bookings(user_id:int, session:Session=Depends(get_db)):
    user=session.get(User,user_id)
    if not user:
        raise  HTTPException(status_code=404,detail="User not found")
    bookings= session.exec(select(Bookings).filter(Bookings.user_id == user_id)).all()
    categorized_bookings ={"men":[],"women":[],"others":[]}
    for booking in bookings:
        cloth_type =cloth_types.get(booking.cloth_type_id)
        if cloth_type:
            category = cloth_type["category"]
            categorized_bookings[category].append({"cloth_type":cloth_type["name"]})
    return {"user":user.name, "bookings":categorized_bookings}    