from pydantic import BaseModel


class UserValidator(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    email: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str
