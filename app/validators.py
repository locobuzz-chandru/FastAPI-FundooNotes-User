import string

from pydantic import BaseModel, EmailStr, constr, field_validator


class UserValidator(BaseModel):
    username: constr(strip_whitespace=True, min_length=4)
    password: str
    first_name: constr(strip_whitespace=True, min_length=1)
    last_name: constr(strip_whitespace=True, min_length=1)
    email: EmailStr

    class Config:
        from_attributes = True

    @field_validator("password")
    def validate_password(cls, password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isupper() for char in password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one digit")
        if not any(char in string.punctuation for char in password):
            raise ValueError("Password must contain at least one special character")
        return password


class UserLogin(BaseModel):
    username: constr(strip_whitespace=True, min_length=4)
    password: constr(strip_whitespace=True, min_length=8)
