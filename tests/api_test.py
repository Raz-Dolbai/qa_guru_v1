import json
from http import HTTPStatus
import pytest
import requests
import random

from app.models.user import UserData, UserCreate


# NAME_USERS = ["Ivan", "Petr", "Vlodimir"]
# JOB_USERS = ["CEO", "CTO", "CPO"]

# Поправить тест test_user_nonexistent_values - добавить фикстуру туда, брать max(id)+1 и чекать
# тест на создание post
# тест на delete: должны иметь клиентов или id его, предусловие создать клиента. внутри в теле теста его удалить
# тест на patch созданный пользователь
# тест на 405 - method not allowe - отправка get на post
# предусловия - может быть json - может быть фикстура которая вернет json, словарик прямо в тесте

class TestUser:

    @pytest.fixture(scope="module")
    def fill_test_data(self, base_url):
        with open("users.json") as f:
            test_data_users = json.load(f)
        api_users = []
        for user in test_data_users:
            response = requests.post(f"{base_url}/api/users/", json=user)
            api_users.append(response.json())
        user_ids = list(map(lambda x: x["id"], api_users))
        yield user_ids
        for user_id in user_ids:
            requests.delete(f"{base_url}/api/users/{user_id}")

    @pytest.fixture
    def users(self, base_url):
        response = requests.get(f"{base_url}/api/users/")
        assert response.status_code == HTTPStatus.OK
        return response.json()

    @pytest.mark.usefixtures("fill_test_data")
    def test_users(self, base_url):
        response = requests.get(f"{base_url}/api/users")
        assert response.status_code == HTTPStatus.OK
        user_list = response.json()
        for user in user_list:
            UserData.model_validate(user)

    @pytest.mark.usefixtures("fill_test_data")
    def test_users_no_duplicate(self, users):
        users_ids = list(map(lambda x: x["id"], users))
        assert len(users_ids) == len(set(users_ids))

    def test_get_user(self, base_url, fill_test_data):
        for user_id in (fill_test_data[0], fill_test_data[-1]):
            response = requests.get(f"{base_url}/api/users/{user_id}")
            assert response.status_code == HTTPStatus.OK
            user = response.json()
            UserData.model_validate(user)

    def test_create_user(self, base_url, fake_user):
        response = requests.post(f"{base_url}/api/users", data=json.dumps(fake_user),
                                 headers={"Content-Type": "application/json"})
        assert response.status_code == HTTPStatus.CREATED
        user = response.json()
        UserCreate.model_validate(user)
        assert user["email"] == fake_user["email"], f"Fake email {fake_user['email']}, Response {response.text}"
        assert user["first_name"] == fake_user[
            "first_name"], f"Fake first_name {fake_user['first_name']}, Response {response.text}"
        assert user["last_name"] == fake_user[
            "last_name"], f"Fake email {fake_user['last_name']}, Response {response.text}"
        assert user["avatar"] == fake_user["avatar"], f"Fake avatar {fake_user['avatar']}, Response {response.text}"

    def test_create_user_with_empty_data(self, base_url):
        response = requests.post(f"{base_url}/api/users", data={},
                                 headers={"Content-Type": "application/json"})
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, f"Response {response.text}, {response.status_code}"

    def test_update_all_user_field(self, base_url, create_fake_user):
        user_id = create_fake_user["id"]
        update_data = {"email": "blabla@ya.ru", "first_name": "Antonio", "last_name": "Banderas",
                       "avatar": 'https://picsum.photos/123/321'}
        response = requests.patch(f"{base_url}/api/users/{user_id}", data=json.dumps(update_data))
        assert response.status_code == HTTPStatus.CREATED
        body = response.json()
        assert body["id"] == user_id
        assert body["email"] == update_data["email"]
        assert body["avatar"] == update_data["avatar"]
        assert body["first_name"] == update_data["first_name"]
        assert body["last_name"] == update_data["last_name"]

    def test_update_one_user_field(self, base_url, create_fake_user):
        user_id = create_fake_user["id"]
        update_data = {"last_name": "Banderas"}
        response = requests.patch(f"{base_url}/api/users/{user_id}", data=json.dumps(update_data))
        assert response.status_code == HTTPStatus.CREATED
        body = response.json()
        assert body["id"] == user_id
        assert body["email"] == create_fake_user["email"]
        assert body["avatar"] == create_fake_user["avatar"]
        assert body["first_name"] == create_fake_user["first_name"]
        assert body["last_name"] == update_data["last_name"]

    def test_delete_user(self, base_url, create_fake_user):
        user_id = create_fake_user["id"]
        response = requests.delete(f"{base_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.OK
        body = response.json()
        assert body["message"] == "user delete successful"

    def test_get_user_nonexistent_value(self, base_url, max_users_id):
        response = requests.get(f"{base_url}/api/users/{max_users_id + 1}")
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_delete_user_nonexistent_value(self, base_url, max_users_id):
        response = requests.delete(f"{base_url}/api/users/{max_users_id + 1}")
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_update_user_nonexistent_value(self, base_url, max_users_id):
        update_data = {"last_name": "Banderas"}
        response = requests.patch(f"{base_url}/api/users/{max_users_id + 1}", data=json.dumps(update_data))
        assert response.status_code == HTTPStatus.NOT_FOUND

    @pytest.mark.parametrize("user_id", [0, "b", "blabla"])
    def test_update_user_not_valid_id(self, base_url, user_id):
        update_data = {"last_name": "Banderas"}
        response = requests.patch(f"{base_url}/api/users/{user_id}", data=json.dumps(update_data))
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    @pytest.mark.parametrize("user_id", [0, "b", "blabla"])
    def test_delete_user_not_valid_id(self, base_url, user_id, fake_user):
        response = requests.delete(f"{base_url}/api/users/{user_id}", data=json.dumps(fake_user))
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_method_not_allowed(self, base_url):
        response = requests.post(f"{base_url}/api/users/1")
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    def test_get_after_created_user(self, base_url, create_fake_user):
        user_id = create_fake_user["id"]
        response = requests.get(f"{base_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.OK
        body = response.json()
        assert body["id"] == user_id
        assert body["email"] == create_fake_user["email"]
        assert body["avatar"] == create_fake_user["avatar"]
        assert body["first_name"] == create_fake_user["first_name"]
        assert body["last_name"] == create_fake_user["last_name"]

    def test_get_after_update_user(self, base_url, update_created_user):
        user_id = update_created_user["id"]
        response = requests.get(f"{base_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.OK
        body = response.json()
        assert body["id"] == user_id, f"response {response.text}"
        assert body["email"] == update_created_user["email"]
        assert body["avatar"] == update_created_user["avatar"]
        assert body["first_name"] == update_created_user["first_name"]
        assert body["last_name"] == update_created_user["last_name"]

    def test_get_after_delete_user(self, base_url, create_fake_user):
        user_id = create_fake_user["id"]
        response_delete = requests.delete(f"{base_url}/api/users/{user_id}")
        assert response_delete.status_code == HTTPStatus.OK
        response_get = requests.get(f"{base_url}/api/users/{user_id}")
        assert response_get.status_code == HTTPStatus.NOT_FOUND, f"Response {response_get.text}, {response_get.status_code}"
