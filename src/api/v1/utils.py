from aioredis import Redis
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core import s3
from core.auth_params import oauth2_scheme
from db.posgres import get_session
from db.redis import get_redis
from schemas.users_schemas import ServiceAvailabiltySchema
from services.userservice import UserService
from services.utils_internal_service import UtilsInternalService

router = APIRouter()


@router.get(
    '/ping',
    summary='Ping db',
    description='Ping database if it work',
    response_model=ServiceAvailabiltySchema,
)
async def ping_db(
        access_token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_session),
        redis: Redis = Depends(get_redis),
):
    user_id = await UserService().check_user_auth(db, access_token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    internal_service = UtilsInternalService()
    service_availability = ServiceAvailabiltySchema(
        redis=await internal_service.check_redis(redis),
        db=await internal_service.check_db(db),
        s3=await internal_service.check_s3(s3.storage_client)
    )
    return service_availability
