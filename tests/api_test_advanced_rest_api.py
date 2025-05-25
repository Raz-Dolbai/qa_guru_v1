from http import HTTPStatus
from deepdiff import DeepDiff
import pytest
import requests

from app.models.user import UserData, UserCreate
from models.object_models import ResponseGetUser


def test_get_user(reqresin):
    result = ResponseGetUser(response=reqresin.get("/api/users/2"))
    expected = ResponseGetUser()
    ddiff = DeepDiff(result, expected, ignore_order=True).affected_paths
    assert not ddiff
    assert expected.support_url == result.support_url
    assert expected.json == result.json


class TestUser:

    def test_get_user_with_object_model(self, reqress_client):
        result = reqress_client.get_user(2)
        expected = ResponseGetUser()
        ddiff = DeepDiff(result, expected, ignore_order=True).affected_paths
        assert not ddiff
        assert expected.support_url == result.support_url
        assert expected.json == result.json

    def test_create_user(self, reqress_client, fake_user):
        response = reqress_client.create_user(UserCreate.model_dump(fake_user))
        assert response.status_code == HTTPStatus.CREATED
        result = UserData.model_validate(**response.json())
        assert result.email == fake_user.email
        assert result.first_name == fake_user.first_name
        assert result.last_name == fake_user.last_name
        assert result.avatar == fake_user.avatar

    def test_create_user_with_empty_data(self, reqress_client):
        result = reqress_client.create_user({})
        assert result.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_update_all_user_field(self, reqress_client, create_fake_user):
        user_id = create_fake_user.id
        update_data = UserData(email="blabla@ya.ru", first_name="Antonio", last_name="Banderas",
                               avatar='https://picsum.photos/123/321')
        response = reqress_client.update_user(update_data.model_dump())
        assert response.status_code == HTTPStatus.CREATED
        result = UserData.model_validate(**response.json())
        assert result.id == user_id
        assert result.email == update_data.email
        assert result.avatar == update_data.avatar
        assert result.first_name == update_data.first_name
        assert result.last_name == update_data.last_name

    def test_update_one_user_field(self, reqress_client, create_fake_user):
        user_id = create_fake_user.id
        update_data = {"last_name": "Banderas"}
        response = reqress_client.update_user(payload=update_data, user_id=user_id)
        assert response.status_code == HTTPStatus.CREATED
        result = UserData.model_validate(**response.json())
        assert result.id == user_id
        assert result.email == create_fake_user.email
        assert result.avatar == create_fake_user.avatar
        assert result.first_name == create_fake_user.first_name
        assert result.last_name == update_data["last_name"]

    def test_delete_user(self, reqress_client, create_fake_user):
        user_id = create_fake_user.id
        response = reqress_client.delete(user_id)
        assert response.status_code == HTTPStatus.OK
        body = response.json()
        assert body.get("message", None) == "user delete successful"

    def test_get_user_nonexistent_value(self, reqress_client, max_users_id):
        response = reqress_client.get_user(max_users_id + 1)
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_delete_user_nonexistent_value(self, reqress_client, max_users_id):
        response = reqress_client.delete_user(max_users_id + 1)
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_update_user_nonexistent_value(self, reqress_client, max_users_id):
        update_data = {"last_name": "Banderas"}
        response = reqress_client.update_user(payload=update_data, user_id=max_users_id + 1)
        assert response.status_code == HTTPStatus.NOT_FOUND

    @pytest.mark.parametrize("user_id", [0, "b", "blabla"])
    def test_update_user_not_valid_id(self, reqress_client, user_id):
        update_data = {"last_name": "Banderas"}
        response = reqress_client.update_user(payload=update_data, user_id=user_id)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    @pytest.mark.parametrize("user_id", [0, "b", "blabla"])
    def test_delete_user_not_valid_id(self, reqress_client, user_id):
        response = reqress_client.delete_user(user_id=user_id)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_method_not_allowed(self, base_url):
        response = requests.post(f"{base_url}/api/users/1")
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    def test_get_after_created_user(self, reqress_client, create_fake_user):
        user_id = create_fake_user.id
        response = reqress_client.get(user_id)
        assert response.status_code == HTTPStatus.OK
        body = response.json()
        UserData.model_validate(body)
        response_model = UserData(**body)
        assert response_model.id == user_id
        assert response_model.email == create_fake_user.email
        assert response_model.avatar == create_fake_user.avatar
        assert response_model.first_name == create_fake_user.first_name
        assert response_model.last_name == create_fake_user.last_name

    def test_get_after_update_user(self, reqress_client, update_created_user):
        user_id = update_created_user.id
        response = reqress_client.get(user_id)
        assert response.status_code == HTTPStatus.OK
        body = response.json()
        UserData.model_validate(body)
        response_model = UserData(**body)
        assert response_model.id == user_id
        assert response_model.email == update_created_user.email
        assert response_model.avatar == update_created_user.avatar
        assert response_model.first_name == update_created_user.first_name
        assert response_model.last_name == update_created_user.last_name

    def test_get_after_delete_user(self, reqress_client, create_fake_user):
        user_id = create_fake_user.id
        response_delete = reqress_client.delete(user_id)
        assert response_delete.status_code == HTTPStatus.OK
        response_get = reqress_client.get(user_id)
        assert response_get.status_code == HTTPStatus.NOT_FOUND
