import os
import uuid
from fastapi import UploadFile

def save_file_to_disk(file: UploadFile, upload_dir: str = "./uploads/videos") -> str:
    """
    Saves the uploaded file to disk and returns the relative file URL.
    """
    try:
        # Ensure the upload directory exists
        os.makedirs(upload_dir, exist_ok=True)

        # Generate a unique filename
        unique_filename = f"{uuid.uuid4()}{os.path.splitext(file.filename)[1]}"

        # Full path to save the file
        file_path = os.path.join(upload_dir, unique_filename)

        # Save the file to disk
        with open(file_path, "wb") as f:
            f.write(file.file.read())

        # Construct the relative URL (ensure no double prefix)
        return f"/uploads/videos/{unique_filename}"
    except Exception as e:
        print(f"Error saving file: {e}")
        return None
