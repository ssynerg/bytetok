from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.database import get_db
from app.auth.dependencies import get_current_user
from app.video.models import Video, Comment
from app.auth.models import User, followers

router = APIRouter()


@router.get("/")
async def get_profile_data(
    db: Session = Depends(get_db),  
    current_user=Depends(get_current_user)
):
    """
    Fetch the profile data for the logged-in user.
    """
    try:
        # Fetch the user's videos
        videos = (
            db.query(Video)
            .filter(Video.uploader_id == current_user.id)
            .order_by(Video.created_at.desc())
            .all()
        )

        # Calculate user stats
        total_videos = db.query(Video).filter(Video.uploader_id == current_user.id).count()
        total_likes = db.query(func.sum(Video.likes)).filter(Video.uploader_id == current_user.id).scalar() or 0
        total_views = db.query(func.sum(Video.views)).filter(Video.uploader_id == current_user.id).scalar() or 0
        total_comments = (
            db.query(func.count(Comment.id))
            .join(Video, Video.id == Comment.video_id)
            .filter(Video.uploader_id == current_user.id)
            .scalar() or 0
        )

        # Count followers and following using SQL
        followers_count = (
            db.query(User)
            .join(followers, followers.c.followed_id == User.id)
            .filter(followers.c.follower_id == current_user.id)
            .count()
        )
        following_count = (
            db.query(User)
            .join(followers, followers.c.follower_id == User.id)
            .filter(followers.c.followed_id == current_user.id)
            .count()
        )

        return {
            "user": {
                "id": current_user.id,
                "username": current_user.username,
                "email": current_user.email,
                "followersCount": followers_count,
                "followingCount": following_count,
            },
            "videos": [video.to_dict() for video in videos],
            "stats": {
                "totalVideos": total_videos,
                "totalLikes": total_likes,
                "totalViews": total_views,
                "totalComments": total_comments,
            },
        }
    except Exception as e:
        print(f"Error fetching profile data: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{user_id}")
async def get_user_videos(
    user_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    current_user=Depends(get_current_user),
):
    """
    Fetch videos and analytics for a specific user.
    """
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized access")

    try:
        # Fetch videos for the user
        videos = (
            db.query(Video)
            .filter(Video.uploader_id == user_id)
            .order_by(Video.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        # Analytics
        total_videos = db.query(Video).filter(Video.uploader_id == user_id).count()
        total_likes = db.query(func.sum(Video.likes)).filter(Video.uploader_id == user_id).scalar() or 0
        total_views = db.query(func.sum(Video.views)).filter(Video.uploader_id == user_id).scalar() or 0
        total_comments = (
            db.query(func.count(Comment.id))
            .join(Video, Video.id == Comment.video_id)
            .filter(Video.uploader_id == user_id)
            .scalar() or 0
        )

        analytics = {
            "totalVideos": total_videos,
            "totalLikes": total_likes,
            "totalViews": total_views,
            "totalComments": total_comments,
        }

        return {"videos": [video.to_dict() for video in videos], "analytics": analytics}
    except Exception as e:
        print(f"Error fetching user videos: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
