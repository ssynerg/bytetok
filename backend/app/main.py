from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.auth.routes import router as auth_router  # Import the auth router
from app.video.routes import router as video_router  # Import the video router
from app.profile.routes import router as profile_router
from app.live_stream.routes import router as live_stream_router
import os

app = FastAPI(title="TikTok Clone Backend", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.40.19:3000"],  # Replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Ensure the upload directory exists
UPLOAD_DIR = "./uploads/videos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Mount the static file route to serve uploaded files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(video_router, prefix="/video", tags=["video"])
app.include_router(profile_router, prefix="/profile", tags=["profile"])
app.include_router(live_stream_router, prefix="/live-stream", tags=["live_stream"])

@app.get("/")
def read_root():
    """Health check route."""
    return {"message": "Welcome to TikTok Clone Backend"}

# Print all registered routes at startup
@app.on_event("startup")
async def print_routes():
    print("Registered Routes:")
    for route in app.routes:
        if hasattr(route, "methods"):  # Check if the route has HTTP methods
            print(f"Path: {route.path}, Methods: {route.methods}")
        else:
            print(f"Path: {route.path}, Mounted App: {type(route.app).__name__}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
