import logging
import uuid
from os import path
from typing import List, Optional

from fastapi import status, HTTPException
from sqlalchemy import func, select, update, exists
from sqlalchemy.ext.asyncio import AsyncSession
import hashlib
from core.config import settings
from models.files import Files
from core import s3
from schemas.users_schemas import File
from copy import deepcopy

_logger = logging.getLogger(__name__)


class FileService:

    async def upload_file(self, file, session):
        filename = file.filename
        file_path = f"media/{file.filename}"
        file_bytes = file.file.read()
        size = len(file_bytes)
        file_to_create = Files(
            path=file_path,
            filename=filename,
            size=size,
            bucket=settings.BUCKET_NAME,
        )
        session.add(file_to_create)
        await session.commit()
        s3.storage_client.upload_fileobj(file_bytes, settings.BUCKET_NAME, filename)

    async def dowload_file(self, filename, session, redis_service):
        statement = select(exists().where(Files.filename == filename))
        results = await session.execute(statement=statement)
        if not results.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found",
            )
        key = redis_service.build_key("download", [filename])
        cached_file_data = await redis_service.get_value(key)
        file_bytes = None
        if not cached_file_data:
            get_object_response = s3.storage_client.get_object(Bucket=settings.BUCKET_NAME, Key=filename)
            file_bytes = get_object_response['Body'].read()
            await redis_service.set_value(key, {"file_data": list(file_bytes)})
        else:
            data_from = cached_file_data.get("file_data")
            file_bytes = bytes(data_from)
        return file_bytes

    async def get_files_info(self, session: AsyncSession, page: int, size: int, redis_service):
        offset = 0
        limit = size
        if page:
            offset = (page - 1) * size
            limit = page * size
        response = []
        key = redis_service.build_key("get_file", [page, size])
        cached_file_data = await redis_service.get_value(key)
        if not cached_file_data:
            statement = select(Files).offset(offset).limit(limit)
            results = await session.execute(statement=statement)
            statistics = results.fetchall()
            for statistic in statistics:
                response.append(File(
                    created_at=str(statistic[0].created_at),
                    name=statistic[0].filename,
                    size=statistic[0].size,
                ))
            await redis_service.set_value(key, [file.dict()for file in response])
        else:
            for cache_file in cached_file_data:
                response.append(
                    File(**cache_file)
                )
        return response
