from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Optional, List
import enum

from api.models.base import Base



class RoleEnums(enum.Enum):
    ADMIN = "admin"
    AI_AGENT = "agent"
    USER = "user"
    CUSTOMER = "client"

class Role(BaseModel):
    name: str = Field(..., description="Name of the role from a list of choices", choices=[e.value for e in RoleEnums])
    permissions: List[str] = Field(..., description="List of permissions associated with the role")

class User(Base):
    username: str = Field(..., description="Username of the user")
    email: EmailStr = Field(..., description="Email address of the user")
    full_name: Optional[str] = Field(None, description="Full name of the user")
    roles: Optional[List[RoleEnums]] = Field(default_factory=lambda: [RoleEnums.USER.value], description="List of roles assigned to the user")
    model_config = ConfigDict(
        populate_by_name=True,
    )
    
class UserInDB(User):
    password: str = Field(..., description="Password of the user")
    
class PasswordResetRequest(BaseModel):
    email: EmailStr = Field(..., description="Email address of the user requesting password reset")
    
class PasswordChange(BaseModel):
    current_password: str = Field(..., description="Current password of the user")
    new_password: str = Field(..., description="Current password of the user")
    confirm_password: str = Field(..., description="New password for the user")
    
class Token(BaseModel):
    access_token: str = Field(..., description="Access token for the user")
    token_type: str = Field("bearer", description="Type of the token, usually 'bearer'")
    
class TokenData(BaseModel):
    username: str = Field(..., description="Username of the user associated with the token")
    roles: Optional[List[str]] = Field(None, description="List of roles associated with the user")