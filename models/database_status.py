from pydantic import BaseModel


class DatabaseStatus(BaseModel):
    status: bool

