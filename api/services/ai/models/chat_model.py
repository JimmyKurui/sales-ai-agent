from pydantic import BaseModel, Field

class InputMessage(BaseModel):
    """ Represents a chat message from a human user. """
    message: str = Field(..., description="Message content from the user.")