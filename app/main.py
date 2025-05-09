from fastapi import FastAPI
from routers import request, master, user, service
from db.database import create_table
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_table()
    print("Таблицы созданы, если не существовали")
    yield
    print("Приложение завершает работу.")

app = FastAPI(lifespan=lifespan)

app.include_router(request.router)
app.include_router(master.router)
app.include_router(user.router)
app.include_router(service.router)

@app.get("/healthcheck")
async def root():
    return {"message": "Hello VogueStyle!"}

