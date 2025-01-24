import json

import pytest
import requests
import random


NAME_USERS = ["Ivan", "Petr", "Vlodimir"]
JOB_USERS = ["CEO", "CTO", "CPO"]


class TestUser:
    @pytest.mark.parametrize("user_id, expected_email", [
        (2, "janet.weaver@reqres.in"),
    ])
    def test_user_data_successful(self, user_id, expected_email, base_url):
        endpoint = "/api/users/{}".format(user_id)
        response = requests.get(base_url + endpoint)
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
        body = response.json()
        assert "data" in body, "Response body does not contain 'data' key"
        data = body["data"]
        assert data["id"] == user_id, f"Expected id {user_id}, but got {data['id']}"
        assert data["email"] == expected_email, f"Expected email {expected_email}, but got {data['email']}"

    @pytest.mark.parametrize("user_id", [random.randint(10000, 30000) for el in range(3)])
    def test_user_data_unsuccessful(self, user_id, base_url):
        endpoint = "/api/users/{}".format(user_id)
        response = requests.get(base_url + endpoint)
        assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"
        body = response.json()
        assert body == {}, f"Expected value {{}}, but got {body}"


class TestRegister:
    @pytest.mark.parametrize("email, expected_token", [("eve.holt@reqres.in", "QpwL5tke4Pnpja7X4")])
    def test_user_register_successful(self, email, expected_token, base_url):
        endpoint = "/api/register"
        body = {
            "email": email,
            "password": "pistol"
        }
        response = requests.post(base_url + endpoint, data=json.dumps(body), headers={"Content-Type": "application/json"})
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
        data = response.json()
        assert data["token"] == expected_token, f"Expected token {expected_token}, but got {data['token']}"

    @pytest.mark.parametrize("email, password, expected_message", [("eve.holt@reqres.in", "", "Missing password"),
                                                                   ("", "pistol", "Missing email or username"),
                                                                   ("", "", "Missing email or username"),
                                                                   ("blablauser", "pistol",
                                                                    "Note: Only defined users succeed registration")])
    def test_register_unsuccessful(self, email, password, expected_message, base_url):
        endpoint = "/api/register"
        body = {
            "email": email,
            "password": password
        }
        response = requests.post(base_url + endpoint, data=json.dumps(body), headers={"Content-Type": "application/json"})
        assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
        data = response.json()
        assert data["error"] == expected_message, f"Expected message {expected_message}, but got {data['error']}"


class TestLoginUser:
    @pytest.mark.parametrize("email, password, expected_token",
                             [("eve.holt@reqres.in", "cityslicka", "QpwL5tke4Pnpja7X4")])
    def tests_login_successful(self, email, password, expected_token, base_url):
        endpoint = "/api/login"
        body = {
            "email": email,
            "password": password
        }
        response = requests.post(base_url + endpoint, data=json.dumps(body), headers={"Content-Type": "application/json"})
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
        data = response.json()
        assert data["token"] == expected_token, f"Expected token {expected_token}, but got {data['token']}"

    @pytest.mark.parametrize("email, password, expected_message", [("eve.holt@reqres.in", "", "Missing password"),
                                                                   ("", "pistol", "Missing email or username"),
                                                                   ("", "", "Missing email or username"),
                                                                   ("blablauser", "pistol",
                                                                    "user not found")])
    def test_login_unsuccessful(self, email, password, expected_message, base_url):
        endpoint = "/api/login"
        body = {
            "email": email,
            "password": password
        }
        response = requests.post(base_url + endpoint, data=json.dumps(body), headers={"Content-Type": "application/json"})
        assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
        data = response.json()
        assert data["error"] == expected_message, f"Expected message {expected_message}, but got {data['error']}"


class TestCrudUser:

    @pytest.mark.parametrize("name, job",
                             [(random.choice(NAME_USERS), random.choice(JOB_USERS))])
    def test_create_user_successful(self, name, job, base_url):
        endpoint = "/api/users"
        body = {
            "name": name,
            "job": job
        }
        response = requests.post(base_url + endpoint, data=json.dumps(body), headers={"Content-Type": "application/json"})
        assert response.status_code == 201, f"Expected status code 200, but got {response.status_code}"
        data = response.json()
        assert data["job"] == job, f"Expected job {job}, but got {data['job']}"
        assert data["name"] == name, f"Expected name {name}, but got {data['name']}"

    @pytest.mark.parametrize("name, job, user_id",
                             [(random.choice(NAME_USERS), random.choice(JOB_USERS), str(random.randint(1, 100)))])
    def test_put_user_successful(self, name, job, user_id, base_url):
        endpoint = "/api/users/{}".format(user_id)
        body = {
            "name": name,
            "job": job
        }
        response = requests.put(base_url + endpoint, data=json.dumps(body), headers={"Content-Type": "application/json"})
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
        data = response.json()
        assert data["job"] == job, f"Expected job {job}, but got {data['job']}"
        assert data["name"] == name, f"Expected name {name}, but got {data['name']}"

    @pytest.mark.parametrize("name, job, user_id",
                             [(random.choice(NAME_USERS), random.choice(JOB_USERS), str(random.randint(1, 100)))])
    def test_patch_user_successful(self, name, job, user_id, base_url):
        endpoint = "/api/users/{}".format(id)
        body = {
            "name": name,
            "job": job
        }
        response = requests.patch(base_url + endpoint, data=json.dumps(body), headers={"Content-Type": "application/json"})
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
        data = response.json()
        assert data["job"] == job, f"Expected job {job}, but got {data['job']}"
        assert data["name"] == name, f"Expected name {name}, but got {data['name']}"

    @pytest.mark.parametrize("id_user", list(map(lambda x: random.randint(1, 100), range(5))))
    def test_delete_user_successful(self, id_user, base_url):
        endpoint = "/api/users/{}".format(id_user)
        response = requests.delete(base_url + endpoint)
        assert response.status_code == 204, f"Expected status code 204, but got {response.status_code}"
