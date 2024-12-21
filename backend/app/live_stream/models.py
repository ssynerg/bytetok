from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from datetime import datetime
from app.database import Base

class LiveStream(Base):
    __tablename__ = "live_streams"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    is_active = Column(Boolean, default=True)
    streamer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)

    streamer = relationship("app.auth.models.User", back_populates="live_streams")

    def to_dict(self):
        """
        Convert LiveStream object to a dictionary.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "streamer_id": self.streamer_id,
            "is_active": self.is_active,
            "started_at": self.started_at.isoformat(),
            "ended_at": self.ended_at.isoformat() if self.ended_at else None,
        }

class LiveStreamCreate(BaseModel):
    title: str
    description: str
