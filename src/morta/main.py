from fastapi import FastAPI

from morta.middlewares.process_time import register_middlewares
from morta.routes.auth_route import router as auth_router

app = FastAPI()

app.include_router(auth_router)

register_middlewares(app);
