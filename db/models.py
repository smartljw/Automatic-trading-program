"""DB 스키마 정의 — SQLAlchemy ORM."""

from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, Text, JSON
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Price(Base):
    """주가 시계열 (TimescaleDB hypertable)."""
    __tablename__ = "prices"
    time = Column(DateTime, primary_key=True)
    stock_code = Column(String(10), primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)


class Trade(Base):
    """매매 이력."""
    __tablename__ = "trades"
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now)
    stock_code = Column(String(10), nullable=False)
    action = Column(String(10))  # BUY | SELL
    quantity = Column(Integer)
    price = Column(Float)
    pnl = Column(Float, default=0.0)
    strategy_name = Column(String(100))
    signal_confidence = Column(Float)
    paper_trade = Column(Boolean, default=True)


class Strategy(Base):
    """전략 메타데이터."""
    __tablename__ = "strategies"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    active = Column(Boolean, default=False)
    config_json = Column(JSON)
    backtest_result = Column(JSON)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class BotMemoryRecord(Base):
    """봇 장기 기억."""
    __tablename__ = "bot_memory"
    id = Column(Integer, primary_key=True, autoincrement=True)
    memory_type = Column(String(50), nullable=False)
    content = Column(JSON)
    created_at = Column(DateTime, default=datetime.now)


class NewsArticle(Base):
    """수집된 뉴스 기사."""
    __tablename__ = "news_articles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_code = Column(String(10))
    title = Column(Text)
    content = Column(Text)
    sentiment = Column(String(20))  # positive | negative | neutral
    sentiment_score = Column(Float)
    published_at = Column(DateTime)
    source = Column(String(50))
    collected_at = Column(DateTime, default=datetime.now)
