from os import getenv
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routers import request, master, user, service, location, certificate, masterschedule, tg
from db.database import create_table, new_session
from dao.tg import create_tg_role


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_table()
    load_dotenv()
    print("Таблицы созданы, если не существовали")
    async with new_session() as session:
        res = await create_tg_role(int(getenv("TG_ADMIN")), 1, session)
        print(res)
    yield
    print("Приложение завершает работу.")

origins = [
    "*"
]

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

app.include_router(request.router)
app.include_router(master.router)
app.include_router(user.router)
app.include_router(service.router)
app.include_router(location.router)
app.include_router(certificate.router)
app.include_router(masterschedule.router)
app.include_router(tg.router)

app.mount("/static", StaticFiles(directory="uploads"), name="static")

@app.get("/healthcheck")
async def root():
    return {"message": "Hello VogueStyle!"}