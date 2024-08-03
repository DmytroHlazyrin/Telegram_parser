from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, unique=True, index=True)
    sender_id = Column(Integer, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String)
    username = Column(String)
    phone_number = Column(String)
    text = Column(Text)
    date = Column(DateTime)
