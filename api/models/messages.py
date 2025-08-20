from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any


class Message(BaseModel):
    id: str = Field(None, alias="_id", description="Unique identifier for the message", ge="6")
    sender: str
    recipient: str
    content: str
    timestamp: Optional[str] = None
    attachments: Optional[List[Dict[str, Any]]] = None