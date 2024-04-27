from pydantic import BaseModel


class ContactUs(BaseModel):
    full_name: str
    email: str
    subject: str
    message: str