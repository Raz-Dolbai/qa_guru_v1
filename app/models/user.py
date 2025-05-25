from pydantic import BaseModel, EmailStr, HttpUrl
from sqlmodel import Field, SQLModel


class User(BaseModel):
    email: EmailStr
    password: str


class UserData(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr
    first_name: str
    last_name: str
    avatar: str


class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    avatar: HttpUrl


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    avatar: HttpUrl | None = None


class SupportInfo(BaseModel):
    url: str
    text: str


class ResponseModel(BaseModel):
    data: UserData
    support: SupportInfo


class UserRegister(BaseModel):
    id: int
    token: str

# class UserUpdate(BaseModel):
#     job: str
#     name: str
#     updatedAt: str
