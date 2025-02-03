import logging
from contextlib import asynccontextmanager

import dotenv

dotenv.load_dotenv()
import uvicorn
from fastapi import FastAPI
from app.routers import status, users
from app.database.engine import create_db_and_tables
from fastapi_pagination import add_pagination


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.warning("On startup")
    create_db_and_tables()  # не создаст таблицы если они уже есть
    yield
    logging.warning("On shutdown")


app = FastAPI(lifespan=lifespan)
app.include_router(status.router)
app.include_router(users.router)
add_pagination(app)

# To run this app, use the following command in your terminal:
# uvicorn filename:app --reload

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
