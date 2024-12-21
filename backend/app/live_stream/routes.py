from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.auth.dependencies import get_current_user
from app.live_stream.models import LiveStream
from app.live_stream.schemas import LiveStreamCreate  # Import the schema

router = APIRouter()

@router.post("/start")
async def start_live_stream(
    stream_data: LiveStreamCreate,  # Automatically parses and validates JSON body
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # Check if the user already has an active live stream
    active_stream = (
        db.query(LiveStream)
        .filter(LiveStream.streamer_id == current_user.id, LiveStream.is_active == True)
        .first()
    )
    if active_stream:
        raise HTTPException(status_code=400, detail="You already have an active live stream.")

    # Create new stream
    new_stream = LiveStream(
        title=stream_data.title,
        description=stream_data.description,
        streamer_id=current_user.id,
    )
    db.add(new_stream)
    db.commit()
    db.refresh(new_stream)
    return {"message": "Live stream started successfully", "stream": new_stream}

@router.post("/stop")
async def stop_live_stream(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Stop an active live stream.
    """
    # Find the active live stream for the user
    active_stream = (
        db.query(LiveStream)
        .filter(LiveStream.streamer_id == current_user.id, LiveStream.is_active == True)
        .first()
    )
    if not active_stream:
        raise HTTPException(status_code=404, detail="No active live stream found.")

    # Mark the live stream as inactive and record the end time
    active_stream.is_active = False
    active_stream.ended_at = datetime.utcnow()
    db.commit()

    return {"message": "Live stream stopped successfully"}


@router.get("/")
async def get_active_streams(db: Session = Depends(get_db)):
    """
    Get all active live streams.
    """
    streams = db.query(LiveStream).filter(LiveStream.is_active == True).all()
    return {"streams": [stream.to_dict() for stream in streams]}
