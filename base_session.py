from requests import Session


class BaseSession(Session):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.base_url = kwargs.pop("base_url", None)
        self.headers.update({"x-api-key": "reqres-free-v1"})

    def request(self, method, url, **kwargs):
        url = self.base_url+url
        return super().request(method, url, **kwargs)
