from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, Boolean

from core.database import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), unique=True)
    password = Column(String, nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100), nullable=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
