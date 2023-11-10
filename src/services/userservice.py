import hashlib
import logging
import uuid
from datetime import datetime

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import delete, exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.constants import TokenType
from models.users import Tokens, Users
from schemas.users_schemas import TokenSchema, User

_logger = logging.getLogger(__name__)


class UserService:

    async def create_user(self, user_data: User, session: AsyncSession) -> Users:
        user_password = user_data.password
        user_name = user_data.username
        hash_password = hashlib.pbkdf2_hmac(
            'sha256',
            user_password.encode('utf-8'),
            settings.SAULT.encode('utf-8'),
            100000
        )
        user = Users(
            name=user_name,
            password=str(hash_password),
        )
        session.add(user)
        await session.commit()
        return user

    async def login(self, user_data: OAuth2PasswordRequestForm, session: AsyncSession) -> TokenSchema:
        user_password = user_data.password
        user_name = user_data.username
        statement = select(Users).where(Users.name == user_name)
        results = await session.execute(statement=statement)
        user = results.scalar_one_or_none()
        if not user:
            _logger.info("User not found {user}".format(
                user=user_name,
            ))
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        hash_password = hashlib.pbkdf2_hmac(
            'sha256',
            user_password.encode('utf-8'),
            settings.SAULT.encode('utf-8'),
            100000
        )
        hash_password_str = str(hash_password)
        if not (hash_password_str == user.password):
            _logger.info("Invalid password for {user} passowrd {password}".format(
                password=user_password,
                user=user_name,
            ))
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid password"
            )
        await self._search_if_token_exist(session, user)
        token = uuid.uuid4()
        user_token = Tokens(
            token=str(token),
            user_id=user.id
        )
        session.add(user_token)
        await session.commit()
        return TokenSchema(
            access_token=str(token),
            token_type=str(TokenType.bearer.value),
        )

    async def _search_if_token_exist(self, session: AsyncSession, user_id: Users) -> None:
        statement = select(exists().where(Tokens.user_id == user_id.id))
        results = await session.execute(statement=statement)
        if not results:
            return
        delete(Tokens).where(Tokens.user_id == user_id.id)

    async def check_user_auth(self, session: AsyncSession, token: str) -> int:
        statement = select(Tokens).where(Tokens.token == token)
        results = await session.execute(statement=statement)
        if not results:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token"
            )
        token = results.scalar_one_or_none()
        if datetime.utcnow() > token.expire:
            _logger.info("Token expire {token}".format(token=token))
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token expire"
            )
        return token.user_id
