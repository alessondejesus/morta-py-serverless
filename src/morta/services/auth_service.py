from sqlmodel import Session

from morta.core.security import hash_password
from morta.models.user_model import User
from morta.repositories.auth_repository import create_account as create_account_repository


def create_account(session: Session, name: str, email: str, password: str) -> User:
    return create_account_repository(
        session=session,
        name=name,
        email=email,
        password=hash_password(password)
    )
