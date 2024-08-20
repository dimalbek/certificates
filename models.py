from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime
import pytz

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)

    documents = relationship("Document", back_populates="owner")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False)
    content = Column(String, nullable=False)  # This could store the file path
    uploaded_at = Column(DateTime, default=datetime.datetime.now(
        pytz.timezone('Asia/Almaty')))
    place = Column(String, nullable=True)

    owner = relationship("User", back_populates="documents")