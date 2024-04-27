from sqlmodel import Session
from Database.db import engine
from typing import Generator, Annotated
from Deps.config import settings
from Deps.utils import verify_token_access
from Models.user_models import User
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException,status


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/"
)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    print ("token",token)
    token_data = verify_token_access(token)

    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    print(user)
    return user

def get_paystack_secret_key():
    paystack_secret_key = os.getenv("PAYSTACK_SECRET_KEY")
    if not paystack_secret_key:
        raise HTTPException(status_code=500, detail="Paystack secret key not set")
    return paystack_secret_key
