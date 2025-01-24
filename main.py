import random
import uvicorn
import json
from http import HTTPStatus
from models.user import UserUpdate, SupportInfo, UserRegister, UserData, ResponseModel, User
from fastapi import FastAPI, Body, Response
from models.database_status import DatabaseStatus
from models.paginate_model import PaginateModel
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
from fastapi_pagination import Page, add_pagination, paginate

app = FastAPI()
add_pagination(app)

users: list[UserData] = []
items = [
    PaginateModel(id=el, job=random.choice(["CEO", "CTO", "CPO"]), name=random.choice(["Ivan", "Petr", "Vlodimir"]))
    for el in
    range(200)]


@app.get("/ping")
def ping():
    return Response(status_code=HTTPStatus.OK, media_type="application/json", content='{"message": "pong"}')


@app.get("/health")
def health():
    return DatabaseStatus(status=bool(users))


@app.get("/api/users", response_model=Page[PaginateModel], status_code=HTTPStatus.OK)
def get_users():
    return paginate(items)


@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    custom = next((el for el in users if el["id"] == user_id), None)
    support_info = SupportInfo(
        url="https://contentcaddy.io?utm_source=reqres&utm_medium=json&utm_campaign=referral",
        text="Tired of writing endless social media content? Let Content Caddy generate it for you.",
    )
    if not custom:
        return Response(status_code=HTTPStatus.NOT_FOUND, media_type="application/json",
                        content='{}')
    return ResponseModel(data=custom, support=support_info)


@app.post("/api/register", status_code=HTTPStatus.OK)
def register_user(user_data: User = Body()):
    users_bd = ["eve.holt@reqres.in"]
    if not user_data.email and not user_data.password:
        return Response(status_code=400, media_type="application/json",
                        content='{"error": "Missing email or username"}')
    if not user_data.email:
        return Response(status_code=400, media_type="application/json",
                        content='{"error": "Missing email or username"}')
    if not user_data.password:
        return Response(status_code=400, media_type="application/json",
                        content='{"error": "Missing password"}')

    elif user_data.email in users_bd:
        return UserRegister(id=random.randint(1, 100), token="QpwL5tke4Pnpja7X4")
    else:
        return Response(status_code=400, media_type="application/json",
                        content='{"error": "Note: Only defined users succeed registration"}')


@app.post("/api/login")
def login_user(user_data: User = Body()):
    users_bd = ["eve.holt@reqres.in"]
    if not user_data.email and not user_data.password:
        return Response(status_code=400, media_type="application/json",
                        content='{"error": "Missing email or username"}')
    if not user_data.email:
        return Response(status_code=400, media_type="application/json",
                        content='{"error": "Missing email or username"}')
    if not user_data.password:
        return Response(status_code=400, media_type="application/json", content='{"error": "Missing password"}')

    elif user_data.email in users_bd:
        return UserRegister(token="QpwL5tke4Pnpja7X4")
    else:
        return Response(status_code=400, media_type="application/json", content='{"error": "user not found"}')


@app.put("/api/users/{user_id}")
def put_user(user: UserUpdate = Body()):
    now = datetime.now(timezone.utc)
    formatted_time = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-3]
    return {
        "job": user.job,
        "name": user.name,
        "updatedAt": formatted_time
    }


@app.post("/api/users")
def create_user(user: UserUpdate = Body()):
    now = datetime.now(timezone.utc)
    formatted_time = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-3]
    content = {"job": user.job,
               "name": user.name,
               "id": random.randint(1, 999),
               "updatedAt": formatted_time}
    return JSONResponse(status_code=201, media_type="application/json",
                        content=content)


@app.patch("/api/users/{user_id}")
def patch_user(user: UserUpdate = Body()):
    now = datetime.now(timezone.utc)
    formatted_time = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-3]
    return {
        "job": user.job,
        "name": user.name,
        "updatedAt": formatted_time
    }


@app.delete("/api/users/{user_id}")
def delete_user():
    return Response(status_code=204)


# To run this app, use the following command in your terminal:
# uvicorn filename:app --reload

if __name__ == "__main__":
    with open("users.json", encoding="utf-8") as f:
        users = json.load(f)
    for user in users:
        UserData.model_validate(user)
    uvicorn.run(app, host="0.0.0.0", port=8001)
