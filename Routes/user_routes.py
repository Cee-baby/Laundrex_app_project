from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from Deps.deps import get_db, get_current_user
from Models.user_models import (
    UserCreate,
    User,
    Token,
    UserOutput,
    Message,
    NewPassword,
)  # noqa
from typing import Annotated, Any
from fastapi.security import OAuth2PasswordRequestForm
from Deps.utils import (
    get_password_hash,
    create_token,
    verify_token,
    generate_reset_password_email,
    generate_verification_email,
    send_email,
)
from Routes import crud
from datetime import timedelta
from Deps.config import settings

router = APIRouter(tags=["Authentication"])


@router.post("/register")
async def register(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    # check if user already exists
    db_user = crud.get_user_by_email(session=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # hash the password
    user.password = get_password_hash(user.password)
    print(user.password)
    new_user = User(**user.dict())
    print(new_user)

    # generate token
    email_verification_token = create_token(subject=user.email, type_ops="verify")  # noqa

    print(email_verification_token)
    # send email verification to user
    email_data = generate_verification_email(
        email_to=new_user.email, email=new_user.email, token=email_verification_token # noqa
    )
    print(email_data)

    data = send_email(
        email_to=new_user.email,
        subject=email_data.subject,
        html_content=email_data.html_content
    )
    print(data)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return JSONResponse(status_code=200, content={"message": "User registered successfully", "data": data})


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    print(form_data.username)
    # get user by email
    user = crud.authenticate(
        session=db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="email not verified")

    return Token(access_token=create_token(subject=user.id, type_ops="access"))


@router.post("/verify-email/{token}")
async def verify_email(token: str, db: Annotated[Session, Depends(get_db)]):
    # verify token
    email = verify_token(token=token)

    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")

    user = crud.get_user_by_email(session=db, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )

    user.is_active = True
    db.add(user)
    db.commit()
    db.refresh(user)
    return JSONResponse(status_code=201, content={"message": "Email verified"})


@router.post("/password-recovery/{email}")
async def recover_password(email: str, db: Annotated[Session, Depends(get_db)]):
    "Forgot password flow"
    user = crud.get_user_by_email(session=db, email=email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    password_reset_token = create_token(subject=email, type_ops="reset")

    # create email data
    email_data = generate_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )

    send_email(
        email_to=user.email,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return Message(message="Password recovery email sent")


@router.post("/reset-password/")
def reset_password(
    db: Annotated[Session, Depends(get_db)], body: NewPassword
) -> Message:
    """
    Reset password
    """
    email = verify_token(token=body.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = crud.get_user_by_email(session=db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    hashed_password = get_password_hash(password=body.new_password)
    user.password = hashed_password
    db.add(user)
    db.commit()
    return Message(message="Password updated successfully")


@router.post("/login/get-current-user")
def get_logged_user(
    current_user:  Annotated[Session,Depends (get_current_user)]
) -> User | None:
    """
    Test access token
    """
    data = {
        "id": current_user.id,
        "username": current_user.full_name,
        "email": current_user.email,
        "is_active": current_user.is_active,
        "is_superuser": current_user.is_superuser,
        
    }
    return JSONResponse(status_code=201, content=data)

    # return current_user