from typing import Any, List

from aioredis import Redis
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import Response
from fastapi_pagination import Params
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth_params import oauth2_scheme
from db.posgres import get_session
from db.redis import get_redis
from schemas.users_schemas import File as FileSchema
from services.cache_service import RedisService
from services.fileservice import FileService
from services.userservice import UserService

router = APIRouter()


async def chek_authorization(access_token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_session)):
    user_id = await UserService().check_user_auth(db, access_token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post(
    "/upload",
    status_code=status.HTTP_200_OK,
)
async def file_upload(
        user_id: int = Depends(chek_authorization),
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_session)
):
    await FileService().upload_file(file, db)


@router.get(
    "/dowloand",
    status_code=status.HTTP_200_OK,
)
async def file_dowload(
        file: str,
        user_id: int = Depends(chek_authorization),
        db: AsyncSession = Depends(get_session),
        redis: Redis = Depends(get_redis),
):
    redis_service = RedisService(redis)
    data = await FileService().dowload_file(file, db, redis_service)
    response = Response(content=data)
    response.headers["Content-Disposition"] = f"attachment; filename={file}"
    return response


@router.get(
    '/',
    summary='Get files',
    response_model=List[FileSchema],
)
async def get_files_info(
        user_id: int = Depends(chek_authorization),
        page: Params = Depends(),
        db: AsyncSession = Depends(get_session),
        redis: Redis = Depends(get_redis),
):
    redis_service = RedisService(redis)
    response = await FileService().get_files_info(db, page.page, page.size, redis_service)
    return response
