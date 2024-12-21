from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.models import User
from app.auth.utils import decode_token  # Utility to decode JWT

def get_current_user(authorization: str = Header(...), db: Session = Depends(get_db)) -> User:
    """
    Extracts the current authenticated user based on the JWT token passed in the Authorization header.
    """
    try:
        # Ensure the Authorization header contains "Bearer <token>"
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid token format")
        
        # Extract the token
        token = authorization.split("Bearer ")[1]
        print(f"Extracted Token: {token}")  # Debugging: Log the extracted token

        # Decode the token to extract the payload
        payload = decode_token(token)
        print(f"Decoded Payload: {payload}")  # Debugging: Log the decoded payload

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        
        # Retrieve the user from the database
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        print(f"Authenticated User: {user}")  # Debugging: Log the authenticated user
        return user

    except HTTPException as http_error:
        # Reraise HTTP exceptions with their existing status code and detail
        print(f"HTTP Exception in get_current_user: {http_error.detail}")  # Debugging
        raise http_error
    except Exception as e:
        # Catch all other exceptions and log them
        print(f"Unexpected error in get_current_user: {e}")  # Debugging
        raise HTTPException(status_code=401, detail="Authentication failed")
