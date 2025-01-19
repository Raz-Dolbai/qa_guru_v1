import random
from fastapi import FastAPI, HTTPException, Body, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime, timezone
from fastapi.encoders import jsonable_encoder

app = FastAPI()


class UserData(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: str


class SupportData(BaseModel):
    url: str
    text: str


class ResponseModel(BaseModel):
    data: UserData
    support: SupportData


class User(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):
    job: str
    name: str


@app.get("/api/users/{user_id}", response_model=ResponseModel)
def get_user(user_id: int):
    # Mock data for demonstration purposes
    users = {
        2: {
            "id": 2,
            "email": "janet.weaver@reqres.in",
            "first_name": "Janet",
            "last_name": "Weaver",
            "avatar": "https://reqres.in/img/faces/2-image.jpg",
        }
    }

    support_info = {
        "url": "https://contentcaddy.io?utm_source=reqres&utm_medium=json&utm_campaign=referral",
        "text": "Tired of writing endless social media content? Let Content Caddy generate it for you.",
    }

    user = users.get(user_id)
    if not user:
        # todo improve exception
        return Response(status_code=404, media_type="application/json",
                        content='{}')
        # raise HTTPException(status_code=404, detail={})

    return {
        "data": user,
        "support": support_info,
    }


@app.post("/api/register")
def register_user(user: User = Body()):
    users = {"eve.holt@reqres.in": ""}
    if (not user.email or user.email == "") and (not user.password or user.password == ""):
        return Response(status_code=400, media_type="application/json",
                        content='{"error": "Missing email or username"}')
        # raise HTTPException(status_code=400, detail="Missing email or username")
    if not user.email or user.email == "":
        return Response(status_code=400, media_type="application/json",
                        content='{"error": "Missing email or username"}')
    if not user.password or user.password == "":
        return Response(status_code=400, media_type="application/json",
                        content='{"error": "Missing password"}')
        # raise HTTPException(status_code=400, detail="Missing password")

    elif user.email in users:
        return {
            "id": 4,
            "token": "QpwL5tke4Pnpja7X4"
        }
    else:
        return Response(status_code=400, media_type="application/json",
                        content='{"error": "Note: Only defined users succeed registration"}')
        # raise HTTPException(status_code=400, detail="Note: Only defined users succeed registration")


@app.post("/api/login")
def login_user(user: User = Body()):
    users = {"eve.holt@reqres.in": ""}
    if (not user.email or user.email == "") and (not user.password or user.password == ""):
        return Response(status_code=400, media_type="application/json",
                        content='{"error": "Missing email or username"}')
        # raise HTTPException(status_code=400, detail="Missing email or username")
    if not user.email or user.email == "":
        return Response(status_code=400, media_type="application/json",
                        content='{"error": "Missing email or username"}')
        # raise HTTPException(status_code=400, detail="Missing email or username")
    if not user.password or user.password == "":
        return Response(status_code=400, media_type="application/json", content='{"error": "Missing password"}')
        # raise HTTPException(status_code=400, detail="Missing password")

    elif user.email in users:
        return {
            "token": "QpwL5tke4Pnpja7X4"
        }
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
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
