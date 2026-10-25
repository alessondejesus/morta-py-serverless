from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from morta.database.database import create_db_and_tables
from morta.routes.auth_route import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Executado ao iniciar
    create_db_and_tables()
    yield
    # Executado ao encerrar
    print("Aplicação encerrada")


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    print('dentro do middleware ------')
    return response
