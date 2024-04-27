from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from Deps.utils import verify_payment
from Deps.deps import get_db
from typing import Annotated
from sqlmodel import Session
from Models.user_bookings import BookingsCreate, Bookings

payment_router = APIRouter()

@payment_router.post("/verify-transaction/{ref_id}")
async def verify_transaction(ref_id: str, db: Annotated[Session, Depends(get_db)]):
    """
    Verify the transaction id and provision the user 
    """
    payment_status, data = verify_payment(ref_id)
    if payment_status == True:
        booking = db.get(Bookings,ref_id)
        booking.booking_fulfilled = "COMPLETED"

        db.add(booking)
        db.commit()

        booking = jsonable_encoder(booking)
        return JSONResponse(status_code=201, content= {"message": f"payment sucessfull",  "booking":booking})
