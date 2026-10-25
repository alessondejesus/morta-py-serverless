from contextlib import asynccontextmanager

from fastapi import FastAPI, Response, Request, HTTPException

from morta.models.user import UserCreate


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Executado ao iniciar
    print("Aplicação iniciada")
    yield
    # Executado ao encerrar
    print("Aplicação encerrada")


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    print('dentro do middleware ------')
    return response


@app.get("/users/{id}")
def get_users(id: int, q: str | None = None):
    return {"id": id, "query": q}


@app.post("/users/", response_model=UserCreate)
def create_user(user: UserCreate):
    return {"name": user.name, "email": user.email}


@app.post("/process-xml/")
async def process_xml(request: Request):
    try:
        body = await request.body()

        return Response(
            content=body.decode("utf-8"),
            media_type="application/xml"
        )
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
