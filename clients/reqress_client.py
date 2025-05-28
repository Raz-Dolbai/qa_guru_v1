from base_session import BaseSession
from config import Server
from requests import Response


class Reqres:
    def __init__(self, **kwargs):
        env = kwargs.pop("env", "prod")
        self.session = BaseSession(base_url=Server(env).reqres)

    def get_user(self, user_id: int) -> Response:
        response = self.session.get(f"/api/users/{user_id}")
        return response

    def get_users(self) -> Response:
        response = self.session.get(f"/api/users")
        return response

    def create_user(self, payload: dict) -> Response:
        self.session.headers.update({"Content-Type": "application/json"})
        response = self.session.post("/api/users", json=payload)
        return response

    def update_user(self, payload: dict, user_id: int) -> Response:
        self.session.headers.update({"Content-Type": "application/json"})
        response = self.session.patch(f"/api/users/{user_id}", json=payload)
        return response

    def delete_user(self, user_id: int) -> Response:
        response = self.session.delete(f"/api/users/{user_id}")
        return response
