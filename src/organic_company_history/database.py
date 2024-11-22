"""Storing/loading LLM things in sqllite"""
from sqlalchemy import (
    create_engine,
    Integer,
    String,
    Column,
    DateTime,
    ForeignKey,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

DB_NAME = "organic-company-history.db"

engine = create_engine(f"sqlite:///{DB_NAME}", echo=True)

Base = declarative_base()


class Model(Base):
    __tablename__ = "models"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    base_model = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    conversations = relationship("Conversation", back_populates="model")


class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey("models.id"), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    model = relationship("Model", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    conversation = relationship("Conversation", back_populates="messages")


# create tables
Base.metadata.create_all(engine)

# sesion factory
Session = sessionmaker(bind=engine)
session = Session()
