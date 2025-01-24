from pydantic import BaseModel, EmailStr, HttpUrl


class User(BaseModel):
    email: EmailStr
    password: str


class UserData(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    avatar: HttpUrl


class SupportInfo(BaseModel):
    url: str
    text: str


class ResponseModel(BaseModel):
    data: UserData
    support: SupportInfo


class UserRegister(BaseModel):
    id: int
    token: str


class UserUpdate(BaseModel):
    job: str
    name: str
    updatedAt: str
