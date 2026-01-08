# db/models.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

Base = declarative_base()

class UserPreference(Base):
    __tablename__ = "user_preferences"

    user_id = Column(String, primary_key=True)
    preferences = Column(JSONB, nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow)
