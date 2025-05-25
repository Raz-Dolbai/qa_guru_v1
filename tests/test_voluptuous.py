import requests
from pytest_voluptuous import S
from voluptuous import Schema

BASE_URL = "https://reqres.in"

response_list_users = Schema({
    "page": int,
    "per_page": int,
    "total": int,
    "total_pages": int,
    "data": [
        {
            "id": int,
            "email": str,
            "first_name": str,
            "last_name": str,
            "avatar": str
        }
    ],
    "support": {
        "url": str,
        "text": str
    }
})


def test_response_list_users():
    response = requests.get(BASE_URL + "/api/users", headers={"x-api-key": "reqres-free-v1"})
    assert S(response_list_users) == response.json()
