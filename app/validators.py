from pydantic import BaseModel, EmailStr


class UserValidator(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str
