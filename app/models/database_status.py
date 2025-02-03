from pydantic import BaseModel


class DatabaseStatus(BaseModel):
    database: bool

