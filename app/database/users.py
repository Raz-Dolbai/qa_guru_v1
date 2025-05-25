from ..models.user import UserData, UserCreate
from .engine import engine
from sqlmodel import Session, select
from fastapi import HTTPException
from typing import Iterable


def get_user(user_id: int) -> UserData | None:
    with Session(engine) as session:
        return session.get(UserData, user_id)


def get_users() -> Iterable[UserData]:
    with Session(engine) as session:
        statement = select(UserData)
        return session.exec(statement).all()


def create_user(user: UserData) -> UserData:
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def delete_user(user_id: int):
    with Session(engine) as session:
        user = session.get(UserData, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        session.delete(user)
        session.commit()


def update_user(user_id: int, user: UserData) -> UserData:
    with Session(engine) as session:
        db_user = session.get(UserData, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        user_data = user.model_dump(exclude_unset=True)
        db_user.sqlmodel_update(user_data)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
