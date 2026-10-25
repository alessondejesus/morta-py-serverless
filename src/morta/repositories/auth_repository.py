from sqlmodel import Session, select

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


def get_by_email(session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()
