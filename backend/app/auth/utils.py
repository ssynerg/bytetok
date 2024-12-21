import jwt
from jwt import PyJWTError
from fastapi import HTTPException
from datetime import datetime, timedelta
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Fetch the secret key and algorithm from environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
if SECRET_KEY == "default-secret-key":
    raise RuntimeError("SECRET_KEY is not set. Define it in the .env file.")

ALGORITHM = os.getenv("ALGORITHM", "HS256")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain_password: str) -> str:
    """
    Hash a plain password using bcrypt.
    :param plain_password: The plain password to hash.
    :return: The hashed password.
    """
    return pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    :param plain_password: The plain password to verify.
    :param hashed_password: The hashed password to compare against.
    :return: True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def decode_token(token: str) -> dict:
    """
    Decode a JWT token and return its payload.
    :param token: The JWT token to decode.
    :return: The decoded payload as a dictionary.
    :raises HTTPException: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def create_token(data: dict, expires_delta: timedelta = timedelta(hours=1)) -> str:
    """Create a JWT token."""
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({
            "exp": expire,
            "sub": str(data.get("sub"))  # Ensure `sub` is a string
        })
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        print(f"Error creating token: {e}")  # Debug: Remove in production
        raise HTTPException(status_code=500, detail="Failed to create token")
