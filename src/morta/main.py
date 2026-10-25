from fastapi import FastAPI, Request

from morta.routes.auth_route import router as auth_router

app = FastAPI()

app.include_router(auth_router)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    print('dentro do middleware ------')
    return response
