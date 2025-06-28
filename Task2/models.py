
from sqlalchemy import Column, String, Integer
from uuid import uuid4
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    age = Column(Integer, nullable=False)
