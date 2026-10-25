from fastapi import FastAPI, Request


def register_middlewares(app: FastAPI):
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        response = await call_next(request)
        print("[DEBUG] middleware tracking")
        return response
