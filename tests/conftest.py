import dotenv
import pytest
from faker import Faker
from requests import Response

from app.models.user import UserData

pytest_plugins = ["fixture_sessions"]


@pytest.fixture(scope="session", autouse=True)
def load_env():
    dotenv.load_dotenv()  # загружаем переменные из .env


@pytest.fixture(scope="function")
def fake_user() -> UserData:
    """Возвращает фейкового юзера"""
    fake = Faker()
    fake_data = {
        "email": fake.email(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "avatar": fake.image_url(),
    }
    return UserData(**fake_data)


@pytest.fixture(scope="function")
def create_fake_user(fake_user, reqress_client) -> UserData:
    response = reqress_client.create_user(UserData.model_dump(fake_user))
    body = response.json()
    yield UserData(**body)
    user_id = body["id"]
    reqress_client.delete_user(user_id)


@pytest.fixture(scope="function")
def update_created_user(create_fake_user, reqress_client) -> UserData:
    user_id = create_fake_user.id
    update_data = {"email": "blabla@ya.ru", "first_name": "Antonio", "last_name": "Banderas",
                   "avatar": 'https://picsum.photos/123/321'}
    response = reqress_client.update_user(update_data, user_id)
    body = response.json()
    yield UserData(**body)
    reqress_client.delete_user(user_id)


@pytest.fixture(scope="function")
def max_users_id(reqress_client) -> id:
    response = reqress_client.get_users()
    body = response.json()
    max_id = max(map(lambda x: x["id"], body))
    return max_id


@pytest.fixture(scope="function")
def users(reqress_client) -> Response:
    response = reqress_client.get_users()
    return response


def pytest_addoption(parser):
    parser.addoption("--env", default="dev")


@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")
