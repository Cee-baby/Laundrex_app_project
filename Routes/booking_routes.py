from fastapi import APIRouter,Depends,HTTPException, Query
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from Deps.deps import get_db,get_current_user
from Models.user_bookings import (
    Bookings,
    BookingsCreate
    
)
from Models.user_models import User
from Routes import crud
from datetime import timedelta
from typing import Annotated, List
from fastapi.encoders import jsonable_encoder

booking_router = APIRouter(tags=["Bookings"])


    
cloth_types = {
        "men":{
        "polo":"https://images.pexels.com/photos/2096476/pexels-photo-2096476.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
        "senator-wear":"https://images.pexels.com/photos/6190984/pexels-photo-6190984.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
        "T-shirt":"https://images.pexels.com/photos/996329/pexels-photo-996329.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
        },
        "women":{
            "jumpsuit":"https://images.pexels.com/photos/12375736/pexels-photo-12375736.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            "leggins":"https://images.pexels.com/photos/3076516/pexels-photo-3076516.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            "skirt":"https://images.pexels.com/photos/1007018/pexels-photo-1007018.jpeg",
            "Gown":"https://images.pexels.com/photos/7137418/pexels-photo-7137418.jpeg?auto=compress&cs=tinysrgb&w=600",
        },
        "others":{
            "sweater":"https://images.pexels.com/photos/1183266/pexels-photo-1183266.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            "jeans":"https://images.pexels.com/photos/7764611/pexels-photo-7764611.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            "bedcover":"https://images.pexels.com/photos/1841149/pexels-photo-1841149.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            "singlet":"https://images.pexels.com/photos/4980308/pexels-photo-4980308.jpeg?auto=compress&cs=tinysrgb&w=600",
            "towel":"https://images.pexels.com/photos/4210376/pexels-photo-4210376.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            
        },
    }
@booking_router.get("/get-cloths")
async def get_available_cloths(category: Annotated[str, Query(description="choose the category of cloths interested in.")]):
    if category not in ["men", "women", "others"]:
        raise HTTPException(status_code=404, detail="Wrong Category Provided, Available Options are [men, women, others]")
    if category == "men":
        return cloth_types["men"]
    elif category == "women":
        return cloth_types["women"]
    elif category == "others":
        return cloth_types["others"]

@booking_router.post("/bookings/booking")
async def Book_Laundry(booking:BookingsCreate,current_user: Annotated[User, Depends(get_current_user)], db: Annotated[Session,Depends(get_db)]):
    booking_details = Bookings(**booking.dict())
    # booking_data = {
    #     "user_id": current_user.id,
    #     "full_name": current_user.full_name,
    #     "email": current_user.email,
    #     "is_active": current_user.is_active,
    #     "phonenumber":current_user.phonenumber,
    #     "pickup_date":current_user.pickup_date,
    #     "category":current_user.category,
    #     "price":current_user.price,
    #     "total_quantity":current_user.total_quantity,
    #     "total_price":current_user.total_price,
    #     "address":current_user.address,
    #     "status":current_user.status,
    # },
    if not current_user:
        raise HTTPException(status_code=404,detail="User not found")


    return{"message":f"sucessfully booked ,{booking_details}"}

@booking_router.get("/booking/status/{user_id}" ,  response_model=List[Bookings])
async def get_booking_status(user_id: int, session: Session = Depends(get_db)):
    user = session.exec(Bookings).filter(Bookings.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_bookings =jsonable_encoder(user)
    return user_bookings
    


# @booking_router.get("/user-bookings/{user_id}")
# async def get_user_bookings(user_id:int, session:Session=Depends(get_db)):
#     user=session.get(User,user_id)
#     if not user:
#         raise  HTTPException(status_code=404,detail="User not found")
#     bookings= session.exec(select(Bookings).filter(Bookings.user_id == user_id)).all()
#     categorized_bookings ={"men":[],"women":[],"others":[]}
#     for booking in bookings:
#         cloth_type =cloth_types.get(booking)
#         if cloth_type:
#             category = cloth_type["category"]
#             categorized_bookings[category].append({"cloth_type":cloth_type["name"]})
#     return {"user":user.name, "bookings":categorized_bookings}  


@booking_router.get("/current_user/")
async def get_booking_history(current_user: Annotated[User, Depends(get_current_user)], db: Annotated[Session,Depends(get_db)]):
    if not current_user:
        raise HTTPException(status_code=404, detail="User details not found")

    user = current_user
    booking_history = (db, user.id)

    if booking_history is None:
        return JSONResponse(status_code=404, content={"message": "Booking history not found for this user"})

    return JSONResponse(status_code=200, content={"user_details": {
        "id": current_user.id,
        "fullname": current_user.full_name,
        "email": current_user.email,
        "is_active": current_user.is_active,
        "is_fulfilled": current_user.is_fulfilled
    }, 
    })
    

