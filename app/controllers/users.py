from sqlalchemy.orm import Session

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from app.dependencies.session import define_local_session
from app.dependencies.user import identify_user

from app.schemas.user import UserData

from app.models import User


users_controller: APIRouter = APIRouter(prefix="/users")


@users_controller.get("/current", response_model=UserData)
async def get_current_user(current_user: User = Depends(identify_user)):
    return UserData.from_orm(obj=current_user)

@users_controller.get("/relative", response_model=UserData)
async def get_relative(id: int, current_user: User = Depends(identify_user), session: Session = Depends(define_local_session)):
    user: User | None = session.query(User).\
        filter(
            User.id == id,
            User.family == current_user.family
        ).\
        one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You don't have a relative with given `id`"
        )

    return UserData.from_orm(obj=user)
