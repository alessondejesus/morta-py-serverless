import jwt
from fastapi import status
from sqlmodel import select

from morta.core.security import ALGORITHM, SECRET_KEY, create_access_token, hash_password, verify_password
from morta.models.user_model import User

ACCOUNT = {"name": "Alice", "email": "alice@example.com", "password": "s3cret-pass"}


def register(client, **overrides):
    return client.post("/auth/register", json={**ACCOUNT, **overrides})


def login(client, email=ACCOUNT["email"], password=ACCOUNT["password"]):
    return client.post("/auth/login", json={"email": email, "password": password})


def test_register_returns_created_account_without_password(client):
    response = register(client)

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["id"] is not None
    assert body["name"] == ACCOUNT["name"]
    assert body["email"] == ACCOUNT["email"]
    assert "password" not in body


def test_register_stores_hashed_password(client, session):
    register(client)

    user = session.exec(select(User)).one()
    assert user.password != ACCOUNT["password"]
    assert verify_password(ACCOUNT["password"], user.password)


def test_register_rejects_invalid_email(client):
    response = register(client, email="not-an-email")

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_register_rejects_short_name(client):
    response = register(client, name="ab")

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_login_returns_bearer_token(client):
    register(client)

    response = login(client)

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["token_type"] == "bearer"
    assert jwt.decode(body["access_token"], SECRET_KEY, algorithms=[ALGORITHM])["sub"]


def test_login_with_wrong_password_is_unauthorized(client):
    register(client)

    response = login(client, password="wrong-password")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "invalid credentials"


def test_login_with_unknown_email_is_unauthorized(client):
    response = login(client, email="nobody@example.com")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "invalid credentials"


def test_me_returns_current_user_for_valid_token(client):
    register(client)
    token = login(client).json()["access_token"]

    response = client.get("/auth/me/", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == ACCOUNT["email"]


def test_me_without_token_is_unauthorized(client):
    response = client.get("/auth/me/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_me_with_invalid_token_is_unauthorized(client):
    response = client.get("/auth/me/", headers={"Authorization": "Bearer not-a-jwt"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "invalid token"


def test_me_with_token_for_deleted_user_is_unauthorized(client):
    token = create_access_token(user_id=999)

    response = client.get("/auth/me/", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_hash_password_round_trip():
    hashed = hash_password("another-pass")

    assert hashed != "another-pass"
    assert verify_password("another-pass", hashed)
    assert not verify_password("different", hashed)
