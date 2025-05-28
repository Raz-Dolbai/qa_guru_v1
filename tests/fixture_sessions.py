import pytest

from base_session import BaseSession
from clients.reqress_client import Reqres
from config import Server


@pytest.fixture(scope="session")
def reqresin(env):
    with BaseSession(base_url=Server(env).reqres) as session:
        yield session


@pytest.fixture(scope="session")
def reqress_client(env):
    return Reqres(env=env)