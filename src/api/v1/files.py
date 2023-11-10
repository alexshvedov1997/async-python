from typing import Any, List

from db.posgres import get_session
from fastapi import APIRouter, Depends, status, UploadFile, File, HTTPException
from fastapi_pagination import Params
from sqlalchemy.ext.asyncio import AsyncSession
from services.fileservice import FileService
from fastapi.responses import Response
from schemas.users_schemas import File as FileSchema
from typing import List
from db.redis import get_redis
from aioredis import Redis
from services.cache_service import RedisService
from services.userservice import UserService
from core.auth_params import oauth2_scheme

router = APIRouter()


@router.post(
    "/upload",
    status_code=status.HTTP_200_OK,
)
async def file_upload(
        access_token: str = Depends(oauth2_scheme),
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_session)
):
    user_id = await UserService().check_user_auth(db, access_token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    await FileService().upload_file(file, db)


@router.get(
    "/dowloand",
    status_code=status.HTTP_200_OK,
)
async def file_upload(
        file: str,
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
        access_token: str = Depends(oauth2_scheme),
        page: Params = Depends(),
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
    redis_service = RedisService(redis)
    response = await FileService().get_files_info(db, page.page, page.size, redis_service)
    return response

