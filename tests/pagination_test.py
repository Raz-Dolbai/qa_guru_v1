import pytest
import requests
import math

from http import HTTPStatus
from jsondiff import diff


def test_get_items(base_url):
    endpoint = "/api/users/"
    response = requests.get(base_url + endpoint)
    assert response.status_code == 200
    # Проверяем наличие метаданных пагинации
    data = response.json()
    assert "total" in data
    assert "page" in data
    assert "size" in data
    assert "items" in data


@pytest.mark.parametrize("size", [1, 3, 34, 25, 99, 100])
def test_expected_pages_with_various_size(base_url, size):
    endpoint = "/api/users/"
    response = requests.get(base_url + endpoint, params={"size": size})
    assert response.status_code == HTTPStatus.OK, f"Expected status code 200, but got {response.status_code}"
    body = response.json()
    total = body["total"]
    size = body["size"]
    expected_pages = math.ceil(total / size)
    fact_pages = body["pages"]
    assert fact_pages == expected_pages, f"Values does not match: fact_pages = {fact_pages}, expected_pages = {expected_pages}"


@pytest.mark.parametrize("size", [1, 3, 34, 25, 99, 100])
def test_expected_items_with_various_size(base_url, size):
    endpoint = "/api/users/"
    response = requests.get(base_url + endpoint, params={"size": size})
    assert response.status_code == HTTPStatus.OK, f"Expected status code 200, but got {response.status_code}"
    body = response.json()
    items = body["items"]
    assert len(items) == size, f"Values does not match: items = {items}, size = {size}"


def test_different_objects_on_different_pages(base_url):
    endpoint = "/api/users/"
    response_1 = requests.get(base_url + endpoint, params={"size": 10, "page": 1})
    response_2 = requests.get(base_url + endpoint, params={"size": 10, "page": 2})
    assert response_1.status_code == HTTPStatus.OK, f"Expected status code 200, but got {response_1.status_code}"
    assert response_2.status_code == HTTPStatus.OK, f"Expected status code 200, but got {response_2.status_code}"
    first_json = response_1.json()["items"]
    second_json = response_2.json()["items"]
    json_diff = diff(first_json, second_json, syntax="symmetric")
    assert json_diff != {}, f"Data on different pages is not different"
