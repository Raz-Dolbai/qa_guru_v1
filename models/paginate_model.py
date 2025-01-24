from pydantic import BaseModel


class PaginateModel(BaseModel):
    id: int
    name: str
    job: str
