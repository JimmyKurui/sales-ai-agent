from pydantic import BaseModel, Field, ConfigDict 
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from datetime import datetime, timezone
from typing import Optional


PyObjectId = Annotated[str, BeforeValidator(str)]

class Base(BaseModel):
    id: Optional[PyObjectId] = Field(None, alias="_id", description="Unique identifier for the message")
    created_at: str = Field(datetime.now(timezone.utc).isoformat(), description="Creation timestamp")
    created_by: Optional[str] = Field(None, description="Creator of the record")
    updated_at: str = Field(datetime.now(timezone.utc).isoformat(), description="Last update timestamp")
    updated_by: Optional[str] = Field(None, description="Last updater of the record")
    deleted_at: Optional[str] = Field(None, description="Deletion timestamp")
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )