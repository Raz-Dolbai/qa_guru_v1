import os
import dotenv
import pytest



@pytest.fixture(autouse=True)
def load_env():
    dotenv.load_dotenv()  # загружаем переменные из .env

@pytest.fixture()
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
