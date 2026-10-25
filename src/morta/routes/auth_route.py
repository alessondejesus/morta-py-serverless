from fastapi import APIRouter

from morta.database.database import SessionDep
from morta.schemas.auth_schema import RegisterAccount, RegisteredAccount
from morta.services.auth_service import create_account

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/me")
def get_users(id: int, q: str | None = None):
    return {"id": id, "query": q}


@router.post("/register", response_model=RegisteredAccount)
def register(account: RegisterAccount, session: SessionDep):
    return create_account(session, account.name, account.email, account.password)
