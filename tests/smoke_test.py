import requests
from http import HTTPStatus


def test_service_availability(base_url):
    endpoint = "/ping"
    response = requests.get(base_url + endpoint)
    assert response.status_code == HTTPStatus.OK, f"Expected status code 200, but got {response.status_code}"
    body = response.json()
    assert body["message"] == "pong", f"Expected message pong, but got {body['message']}"


def test_database_health(base_url):
    endpoint = "/health"
    response = requests.get(base_url + endpoint)
    assert response.status_code == HTTPStatus.OK, f"Expected status code 200, but got {response.status_code}"
    body = response.json()
    assert body["database"], f"Expected status True, but got {body['status']}"


def test_non_existent_endpoint(base_url):
    endpoint = "/non_existent_email"
    response = requests.get(base_url + endpoint)
    assert response.status_code == HTTPStatus.NOT_FOUND, f"Expected status code 404, but got {response.status_code}"

