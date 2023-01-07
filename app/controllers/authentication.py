from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from app.dependencies.sessions import define_postgres_session
from app.schemas.authentication import AuthenticationData
from app.schemas.user import UserCreationData
from app.utilities.exceptions.auth import (
    UsernameAlreadyExists,
    WrongPassword,
    WrongUsername,
)
from app.utilities.security.jwt import create_access_token
from core.databases.models import User
from core.databases.services import UserService


authentication_controller: APIRouter = APIRouter(tags=["authentication"])


@authentication_controller.post("/sign-up", response_model=AuthenticationData, status_code=status.HTTP_201_CREATED)
async def sign_up(
    user_data: UserCreationData,
    session: Session = Depends(define_postgres_session),
) -> AuthenticationData:
    user_service: UserService = UserService(session=session)
    user: User | None = user_service.get_by_username(user_data.username)

    if user is not None:
        raise UsernameAlreadyExists(username=user.username)

    user = user_service.create(
        record_data=user_data.dict(),
        password=PasswordHasher().hash(user_data.password),
    )
    access_token: str = create_access_token(user_id=user.id)

    return AuthenticationData(
        access_token=access_token,
        user=user,
    )

@authentication_controller.get("/sign-in", response_model=AuthenticationData)
async def sign_in(
    credentials: HTTPBasicCredentials = Depends(HTTPBasic()),
    session: Session = Depends(define_postgres_session),
) -> AuthenticationData:
    user_service: UserService = UserService(session=session)
    user: User | None = user_service.get_by_username(credentials.username)

    if user is None:
        raise WrongUsername(username=credentials.username)

    try:
        PasswordHasher().verify(hash=user.password, password=credentials.password)
    except VerifyMismatchError:
        raise WrongPassword(username=user.username)

    access_token: str = create_access_token(user_id=user.id)

    return AuthenticationData(
        access_token=access_token,
        user=user,
    )
