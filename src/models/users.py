from datetime import datetime, timedelta

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from .base import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Tokens(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    token = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    expire = Column(DateTime, default=(datetime.utcnow() + timedelta(days=5)))
    user_id = Column(Integer, ForeignKey("users.id"))
