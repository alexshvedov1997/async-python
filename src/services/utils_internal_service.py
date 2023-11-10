import logging
from http import HTTPStatus

from aioredis import ConnectionClosedError, Redis
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings

_logger = logging.getLogger(__name__)


class UtilsInternalService:

    async def check_db(self, session: AsyncSession) -> bool:
        try:
            result = await session.execute("SELECT version()")
            result.scalar()
            return True
        except DatabaseError as error:
            _logger.info("Database error {error}".format(error=error))
        except Exception as error:
            _logger.info("Check db other error {error}".format(error=error))
        return False

    async def check_redis(self, redis: Redis) -> bool:
        try:
            redis.ping()
            return True
        except ConnectionClosedError as error:
            _logger.info("Redis error {error}".format(error=error))
        except Exception as error:
            _logger.info("Check redis other error {error}".format(error=error))
        return False

    async def check_s3(self, client) -> bool:
        response = None
        try:
            response = client.head_bucket(
                Bucket=settings.BUCKET_NAME)
            if response.get("ResponseMetadata", {}).get('HTTPStatusCode') == HTTPStatus.OK:
                return True
        except Exception as error:
            _logger.info("Check s3 other error {error} with response {response}".format(
                error=error,
                response=response,
            ))
        return False
