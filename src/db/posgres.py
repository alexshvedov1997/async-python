from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings

DATABASE_DNS = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}".format(
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    db_name=settings.DB_NAME,
),


engine = create_async_engine(DATABASE_DNS[0], echo=True, future=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False,
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
