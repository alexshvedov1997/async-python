import logging
from logging import config as logging_config

import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_pagination import add_pagination
from core.config import settings
from core.logger import LOGGING
from api.v1 import users, files, utils
import boto3
from core import s3
from core.constants import ENDPOINT
from db import redis
import aioredis


logging_config.dictConfig(LOGGING)

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    s3.session = boto3.Session(
        aws_access_key_id=settings.AWS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_ID,
        region_name=settings.AWS_REGION_NAME,
    )
    s3.storage_client = s3.session.client("s3", endpoint_url=ENDPOINT)
    redis.redis = await aioredis.create_pool(address=(settings.REDIS_HOST, settings.REDIS_PORT))


@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()


add_pagination(app)
app.include_router(users.router, prefix='/api/v1/users', tags=['users'])
app.include_router(files.router, prefix='/api/v1/files', tags=['files'])
app.include_router(utils.router, prefix="/api/v1/utils", tags=["utils"])

if __name__ == '__main__':
    uvicorn.run(
        'app:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
    )
