from pydantic import BaseModel

class LiveStreamCreate(BaseModel):
    title: str
    description: str
