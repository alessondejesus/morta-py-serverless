from sqlmodel import Session

from morta.models.user_model import User


def create_account(session: Session, name: str, email: str, password: str) -> User:
    try:
        user = User(
            name=name,
            email=email,
            password=password
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        return user
    except Exception:
        session.rollback()
        raise
