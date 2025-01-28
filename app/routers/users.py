from typing import Iterable
from fastapi import APIRouter, HTTPException
from http import HTTPStatus
from app.database import users
from app.models.user import SupportInfo, ResponseModel, User, UserRegister, UserUpdate, UserData, UserCreate

router = APIRouter(prefix="/api/users")


@router.get("/", status_code=HTTPStatus.OK)
def get_users() -> Iterable[UserData]:
    return users.get_users()


@router.get("/{user_id}", status_code=HTTPStatus.OK)
def get_user(user_id: int) -> UserData:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user")
    user = users.get_user(user_id)
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return user


@router.post("/", status_code=HTTPStatus.CREATED)
def create_user(user: UserData) -> UserData:
    UserCreate.model_validate(user.model_dump())
    return users.create_user(user)


@router.patch("/{user_id}", status_code=HTTPStatus.CREATED)
def update_user(user_id: int, user: UserData) -> UserData:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user")
    UserUpdate.model_validate(user.model_dump())
    return users.update_user(user_id, user)


@router.delete("/{user_id}", status_code=HTTPStatus.OK)
def delete_user(user_id: int):
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user")
    users.delete_user(user_id)
    return {"message": "user delete successful"}
