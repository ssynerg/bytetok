from sqlalchemy import Column, Boolean, Integer, Text, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Video(Base):
    """
    Video model representing uploaded videos.
    """
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    url = Column(String, nullable=False)
    uploader_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    is_podcast = Column(Boolean, default=False)  # Default to False for non-podcasts
    created_at = Column(DateTime, default=datetime.utcnow)

    # New Attribute: likes
    likes = Column(Integer, default=0)  # Default to 0 likes
    views = Column(Integer, default=0)  # Add views column

    # Relationships
    uploader = relationship("app.auth.models.User", back_populates="videos")
    comments = relationship(
        "app.video.models.Comment",
        back_populates="video",
        cascade="all, delete-orphan",
    )

    def to_dict(self):
        """
        Convert the Video object to a dictionary.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "uploader_id": self.uploader_id,
            "created_at": self.created_at.isoformat(),
            "is_podcast": self.is_podcast,  # Include podcast flag
            "likes": self.likes,  # Include likes in the dictionary
            "views": self.views,
        }


class Comment(Base):
    """
    Comment model representing comments on videos.
    """
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("app.auth.models.User", back_populates="comments")
    video = relationship("app.video.models.Video", back_populates="comments")
