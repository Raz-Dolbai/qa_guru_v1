import os
import dotenv
import pytest
import requests
import json
from faker import Faker


@pytest.fixture(scope="session", autouse=True)
def load_env():
    dotenv.load_dotenv()  # загружаем переменные из .env


@pytest.fixture(scope="session")
def base_url():
    """Возвращает url на котором будем проводить тестирование
    - прокинуть переменную из .env (прим. export ENV=PROD)"""
    try:
        get_env_value = os.environ["ENV"]  # пытаемся прочитать переменную ENV
    except KeyError:
        get_env_value = "TEST"  # если переменной ENV нет, default value = TEST
    if os.getenv(
            get_env_value):  # если переменная get_env_value есть в .env возвращаем ее, если нет возвращаем Exception
        return os.getenv(get_env_value)
    else:
        raise Exception(f"Unknown value of ENV variable {get_env_value}")


@pytest.fixture(scope="function")
def fake_user():
    """Возвращает фейкового юзера"""
    fake = Faker()
    return {
        "email": fake.email(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "avatar": fake.image_url(),
    }


@pytest.fixture(scope="function")
def create_fake_user(fake_user, base_url) -> dict:
    response = requests.post(f"{base_url}/api/users", data=json.dumps(fake_user),
                             headers={"Content-Type": "application/json"})
    body = response.json()
    yield body
    user_id = body["id"]
    requests.delete(f"{base_url}/api/users/{user_id}")


@pytest.fixture(scope="function")
def update_created_user(create_fake_user, base_url) -> dict:
    user_id = create_fake_user["id"]
    update_data = {"email": "blabla@ya.ru", "first_name": "Antonio", "last_name": "Banderas",
                   "avatar": 'https://picsum.photos/123/321'}
    response = requests.patch(f"{base_url}/api/users/{user_id}", data=json.dumps(update_data),
                              headers={"Content-Type": "application/json"})
    body = response.json()
    yield body
    requests.delete(f"{base_url}/api/users/{user_id}")


@pytest.fixture(scope="function")
def max_users_id(base_url) -> id:
    response = requests.get(f"{base_url}/api/users/")
    body = response.json()
    max_id = max(map(lambda x: x["id"], body))
    return max_id
