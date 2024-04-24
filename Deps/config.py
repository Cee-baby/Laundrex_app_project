import secrets
from typing import Annotated, Any, Literal
from fastapi_mail import ConnectionConfig

from pydantic import (
    AnyUrl,
    BeforeValidator,
    computed_field,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    PROJECT_NAME:str="laundrex"
    FRONTEND_URL:AnyUrl="http://localhost:9001/api/v1"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    DOMAIN: str = "localhost"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []
    
    ALGORITHM: str = "HS256"
    EMAIL_RESET_PASSWORD_EXPIRE_MINUTES: int = 10
    EMAIL_VERIFY_EMAIL_EXPIRE_MINUTES: int = 60 * 24 * 8
    EMAILS_FROM_NAME: str = "laundrex"
    EMAILS_FROM_EMAIL: str = "noreply@laundrex.com.ng"
    
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_PORT: int = 465 
    SMTP_HOST: str = "smtp.zeptomail.com"
    SMTP_USER: str = "emailapikey"
    SMTP_PASSWORD: str = "wSsVR613/EL3Dql7njL8Iu44y1lQVFnzEE180FOiv3P7Fv/FpcdtkkfNBFLxG/RNR2ZtQjIXoegokBwF1GZYh98lmwwHACiF9mqRe1U4J3x17qnvhDzNWW5bkRWLLYIAww1pnGRiEsgl+g=="  




settings = Settings()  # type: ignore