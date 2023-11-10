from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .base import Base


class Files(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)
    path = Column(String(255), nullable=False, unique=True)
    filename = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    size = Column(Integer, nullable=False)
    bucket = Column(String(255), nullable=False)
