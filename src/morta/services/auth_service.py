from sqlmodel import Session

from morta.core.security import hash_password, verify_password, create_access_token
from morta.models.user_model import User
from morta.repositories.auth_repository import create_account as create_account_repository, get_by_email
from morta.schemas.auth_schema import TokenResponse
from fastapi import status, HTTPException


def create_account(session: Session, name: str, email: str, password: str) -> User:
    return create_account_repository(
        session=session,
        name=name,
        email=email,
        password=hash_password(password)
    )


def login_account(session: Session, email: str, password: str) -> TokenResponse:
    user = get_by_email(session, email)
    if user is None or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(user.id)
    return TokenResponse(access_token=token)
