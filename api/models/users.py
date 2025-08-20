from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, timezone
from typing import Optional, List
import enum

class RoleEnums(enum.Enum):
    ADMIN = "admin"
    AGENT = "agent"
    USER = "user"

class Role(BaseModel):
    name: str = Field(..., description="Name of the role from a list of choices", choices=[e.value for e in RoleEnums])
    permissions: List[str] = Field(..., description="List of permissions associated with the role")

class User(BaseModel):
    id: str = Field(None, alias="_id", description="Unique identifier for the user", ge="6")
    username: str = Field(..., description="Username of the user")
    password: str = Field(..., description="Password of the user")
    email: str = Field(..., description="Email address of the user")
    full_name: Optional[str] = Field(None, description="Full name of the user")
    created_at: datetime = Field(default=datetime.now(timezone.utc), description="Timestamp when the user was created")
    updated_at: datetime = Field(default=datetime.now(timezone.utc), description="Timestamp when the user was last updated")
    roles: Optional[List[str]] = Field(None, description="List of roles assigned to the user")
    model_config = ConfigDict(
        populate_by_name=True,
    )
    
class UserCreate(BaseModel):
    username: str = Field(..., description="Username of the user")
    email: str = Field(..., description="Email address of the user")
    full_name: Optional[str] = Field(None, description="Full name of the user")
    created_at: Optional[datetime] = Field(default=datetime.now(timezone.utc), description="Timestamp when the user was created")
    updated_at: Optional[datetime] = Field(default=datetime.now(timezone.utc), description="Timestamp when the user was last updated")
    roles: Optional[List[str]] = Field(None, description="List of roles assigned to the user")