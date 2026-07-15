from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100))
    role = Column(String(20))
    # message = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
