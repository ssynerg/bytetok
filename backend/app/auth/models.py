from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

# Association table for followers
followers = Table(
    "followers",
    Base.metadata,
    Column("follower_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("followed_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)

    # Relationships
    videos = relationship(
        "app.video.models.Video",
        back_populates="uploader",
        cascade="all, delete-orphan",
    )
    comments = relationship(
        "app.video.models.Comment",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # Relationships for following and followers
    following = relationship(
        "User",
        secondary=followers,
        primaryjoin=id == followers.c.follower_id,
        secondaryjoin=id == followers.c.followed_id,
        backref="followers",
        lazy="dynamic",
    )

    # Relationship for live streams
    live_streams = relationship(
        "app.live_stream.models.LiveStream",
        back_populates="streamer",
        cascade="all, delete-orphan",
    )
