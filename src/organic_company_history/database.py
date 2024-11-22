"""Storing/loading LLM things in sqllite"""
from sqlalchemy import (
    create_engine,
    Boolean,
    Integer,
    String,
    Column,
    DateTime,
    ForeignKey,
    Text,
    JSON,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import logging

DB_NAME = "organic-company-history.db"
# logging.getLogger("sqlalchemy").setLevel(logging.WARNING)

engine = create_engine(f"sqlite:///{DB_NAME}", echo=False)

Base = declarative_base()


class Model(Base):
    __tablename__ = "models"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    base_model = Column(String, nullable=False)
    modelfile = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    conversations = relationship("Conversation", back_populates="model")
    tools = relationship("Tool", back_populates="model")


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
    response = relationship(
        "Response",
        back_populates="message",
        uselist=False,
        cascade="all, delete-orphan",
    )
    tool_calls = relationship("ToolCall", back_populates="message")


class Response(Base):
    __tablename__ = "responses"
    id = Column(Integer, primary_key=True)
    message_id = Column(
        Integer,
        ForeignKey("messages.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    done_reason = Column(String, nullable=False)
    eval_count = Column(Integer, nullable=False)
    eval_duration = Column(Integer, nullable=False)
    load_duration = Column(Integer, nullable=False)
    prompt_eval_count = Column(Integer, nullable=False)
    prompt_eval_duration = Column(Integer, nullable=False)
    total_duration = Column(Integer, nullable=False)

    message = relationship(
        "Message",
        back_populates="response",
    )


class Tool(Base):
    """Tools that were provided to a model"""

    __tablename__ = "tools"
    id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey("models.id"), nullable=False)
    name = Column(String, nullable=False)
    docstring = Column(Text, nullable=True)
    annotations = Column(Text, nullable=True)
    is_hallucination = Column(Boolean, nullable=False)

    model = relationship("Model", back_populates="tools")
    calls = relationship("ToolCall", back_populates="tool")


class ToolCall(Base):
    """Calls for tools requested by the model."""

    __tablename__ = "tool_calls"
    id = Column(Integer, primary_key=True)
    tool_id = Column(Integer, ForeignKey("tools.id"), nullable=False)
    message_id = Column(Integer, ForeignKey("messages.id"), nullable=False)
    arguments = Column(JSON, nullable=False)

    message = relationship("Message", back_populates="tool_calls", uselist=False)
    result = relationship("ToolResult", back_populates="call", uselist=False)
    tool = relationship("Tool", back_populates="calls")


class ToolResult(Base):
    """Results from a called tool"""

    __tablename__ = "tool_results"
    id = Column(Integer, primary_key=True)
    call_id = Column(Integer, ForeignKey("tool_calls.id"), nullable=False)
    was_error = Column(Boolean, nullable=False)
    value_or_error = Column(Text, nullable=True)

    call = relationship("ToolCall", back_populates="result", uselist=False)


# create tables
Base.metadata.create_all(engine)

# session factory
Session = sessionmaker(bind=engine)
session = Session()
