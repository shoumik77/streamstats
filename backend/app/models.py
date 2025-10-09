from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from app.db import Base

# User model

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# Twitch Connection OAuth
    
class TwitchConnection(Base):
    __tablename__ = "twitch_connections"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    access_token = Column(String)
    refresh_token = Column(String)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="twitch_connections")

# Individual Twitch Broadcasts                    

class Stream(Base):
    __tablename__ = "streams"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index = True)
    twitch_stream_id = Column(String, index=True)
    started_at = Column(DateTime)
    ended_at = Column(DateTime)
    title = Column(String)
    category = Column(String)
    avg_viewers = Column(Integer)
    peak_viewers = Column(Integer)
    total_unique_viewers = Column(Integer)
    stream_duration_min = Column(Integer)

# Viewer info (anonymous)

class Viewer(Base):
    __tablename__ = "viewers"
    id = Column(Integer, primary_key=True)
    twitch_user_id = Column(String, index=True)
    age_bucket = Column(String)
    country = Column(String)
    device = Column(String)

# Viewer info in relation to stream

class StreamViewer(Base):
    __tablename__ = "stream_viewers"
    id = Column(Integer, primary_key=True)
    stream_id = Column(Integer, ForeignKey("streams.id", ondelete="CASCADE"))
    viewer_id = Column(Integer, ForeignKey("viewers.id", ondelete="CASCADE"))
    watch_minutes = Column(Integer)
    chat_messages = Column(Integer)
    first_time_chatter = Column(Boolean, default=False)

# detailed message log

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True)
    stream_id = Column(Integer, ForeignKey("streams.id", ondelete="CASCADE"))
    viewer_id = Column(Integer, ForeignKey("viewers.id", ondelete="CASCADE"))
    ts = Column(DateTime, index=True)
    text = Column(Text)
    sentiment = Column(Float)
    toxicity = Column(Float)

# NL Queries

class NLQuery(Base):
    """
    Stores every natural-language question the streamer asks.
    Keeps record of:
      - the prompt they entered,
      - the SQL query the system generated,
      - the raw/structured results,
      - and the LLM-generated summary answer.
    Useful for analytics history or debugging NLQ behavior.
    """
    __tablename__ = "nl_queries"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    prompt = Column(Text, nullable=False)
    resolved_sql = Column(Text)
    answer = Column(JSONB)
    created_at = Column(DateTime, default=datetime.utcnow)
    
