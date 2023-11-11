import hashlib
from os import path

import pytest
from settings import settings
from sqlalchemy import text


@pytest.fixture
async def create_fake_user(session_db):
    async with session_db.connect() as conn:
        username = "test_user_fake111"
        user_password = "P@ssw0rd!567"
        hash_password = hashlib.pbkdf2_hmac(
            'sha256',
            user_password.encode('utf-8'),
            settings.SAULT.encode('utf-8'),
            100000
        )
        await conn.execute(
            text("INSERT INTO users (name, password) VALUES ('{username}', '{password}')".format(
                username=username,
                password=hash_password.decode('utf-16'),
            )))
        await conn.commit()


@pytest.fixture
async def create_fake_file(session_db):
    async with session_db.connect() as conn:
        size = 20
        filename = "test"
        file_path = path.join("media", 'test')
        await conn.execute(
            text("""INSERT INTO files (path, filename, size, bucket) 
            VALUES ('{path}', '{filename}', {size}, {bucket})""".format(
                path=file_path,
                filename=filename,
                size=size,
                bucket=settings.BUCKET_NAME,
            )))
        await conn.commit()
