from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy.sql import and_
from app.database import get_db
from app.video.models import Video
from app.auth.dependencies import get_current_user
from app.utils import save_file_to_disk

router = APIRouter()

# Upload video route
@router.post("/upload")
async def upload_video(
    title: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Upload a new video with metadata.
    """
    try:
        file_url = save_file_to_disk(file)
        if not file_url:
            raise HTTPException(status_code=500, detail="Failed to save file")

        new_video = Video(
            title=title,
            description=description,
            url=file_url,
            uploader_id=current_user.id,
        )
        db.add(new_video)
        db.commit()
        db.refresh(new_video)

        return {"message": "Video uploaded successfully", "video": new_video.to_dict()}
    except Exception as e:
        print(f"Error uploading video: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during video upload")

@router.get("/feed/for-you")
async def get_for_you_feed(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Fetch videos for the "For You" feed.
    """
    try:
        videos = (
            db.query(Video)
            .order_by(Video.created_at.desc())  # Modify to add recommendation logic if needed
            .offset(skip)
            .limit(limit)
            .all()
        )
        return {"videos": [video.to_dict() for video in videos]}
    except Exception as e:
        print(f"Error fetching For You feed: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/feed/following")
async def get_following_feed(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Fetch videos uploaded by users the current user is following.
    """
    try:
        # Debugging: Check if `current_user.following` exists and is populated
        if not hasattr(current_user, "following"):
            print("Error: `current_user.following` is not defined.")
            raise HTTPException(status_code=500, detail="Following data not available")

        following_user_ids = [user.id for user in current_user.following]

        # Debugging: Log the list of followed user IDs
        print(f"Following user IDs: {following_user_ids}")

        # If no users are followed, return an empty list
        if not following_user_ids:
            return {"videos": []}

        videos = (
            db.query(Video)
            .filter(Video.uploader_id.in_(following_user_ids))
            .order_by(Video.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return {"videos": [video.to_dict() for video in videos]}
    except Exception as e:
        print(f"Error fetching Following feed: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")



# Fetch the "Podcasts" feed
@router.get("/feed/podcasts")
async def get_podcast_feed(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Fetch podcasts for the podcast feed.
    """
    try:
        podcasts = (
            db.query(Video)
            .filter(Video.is_podcast == True)
            .order_by(Video.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return {"videos": [podcast.to_dict() for podcast in podcasts]}
    except Exception as e:
        print(f"Error fetching Podcasts feed: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Like/unlike a video
@router.post("/like/{video_id}")
async def toggle_like_video(video_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Toggle like status for a video.
    """
    try:
        video = db.query(Video).filter(Video.id == video_id).first()
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")

        like = db.query(Video.likes).filter(
            and_(Video.likes.video_id == video_id, Video.likes.user_id == current_user.id)
        ).first()

        if like:
            db.delete(like)
            video.likes -= 1
            message = "Video unliked successfully"
        else:
            new_like = Like(video_id=video_id, user_id=current_user.id)
            db.add(new_like)
            video.likes += 1
            message = "Video liked successfully"

        db.commit()
        return {"message": message, "likes": video.likes}
    except Exception as e:
        print(f"Error toggling like: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Comment on a video
@router.post("/comment/{video_id}")
async def comment_on_video(video_id: int, text: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Add a comment to a video.
    """
    try:
        video = db.query(Video).filter(Video.id == video_id).first()
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")

        new_comment = Comment(video_id=video_id, user_id=current_user.id, text=text)
        db.add(new_comment)
        db.commit()
        return {"message": "Comment added successfully"}
    except Exception as e:
        print(f"Error adding comment: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Fetch comments for a video
@router.get("/comments/{video_id}")
async def get_comments(video_id: int, db: Session = Depends(get_db)):
    """
    Fetch comments for a specific video.
    """
    try:
        comments = db.query(Comment).filter(Comment.video_id == video_id).all()
        return {"comments": [{"id": c.id, "text": c.text, "user_id": c.user_id, "created_at": c.created_at.isoformat()} for c in comments]}
    except Exception as e:
        print(f"Error fetching comments: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
