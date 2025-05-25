import os
from dotenv import load_dotenv

load_dotenv()


class Server:
    def __init__(self, env):
        self.reqres = {"prod": os.getenv("PROD"),
                       "dev": "",
                       "rc": ""}[env]

        self.microservice_1 = {"dev": "https://microservice_1",
                               "prod": "",
                               "rc": ""}[env]

        self.microservice_2 = {"dev": "https://microservice_2",
                               "prod": "",
                               "rc": ""}[env]
