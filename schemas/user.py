from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    username: str
    password: str


class SignUpRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        from_attributes = True
