from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from db.posgres import get_session
from schemas.users_schemas import TokenSchema, User
from services.userservice import UserService

router = APIRouter()


@router.post(
    '/create_user',
    status_code=status.HTTP_201_CREATED,
    summary='Create users',
    description='Endpoint for register users',
)
async def create_users(input_data: User, db: AsyncSession = Depends(get_session)):
    await UserService().create_user(input_data, db)


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=TokenSchema,
)
async def login_user(input_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    data = await UserService().login(input_data, db)
    return data
