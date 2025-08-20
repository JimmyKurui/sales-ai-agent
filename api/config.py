from dotenv import load_dotenv
from typing import Literal, Optional
from pydantic import HttpUrl, BaseModel, Field
from enum import Enum
import os

load_dotenv()

OPENROUTER_API_KEY: str = str(os.getenv("OPENROUTER_API_KEY"))
OPENAI_API_KEY: str = str(os.getenv("OPENAI_API_KEY"))
GROQ_API_KEY: str = str(os.getenv("GROQ_API_KEY"))
MONGODB_URI: str = str(os.getenv("MONGODB_URI"))
MONGODB_NAME: str = str(os.getenv("MONGODB_NAME"))

# ------------------------ AI Configurations ------------------------
class Roles(Enum):
    BRAIN = "brain"
    IMAGE_TO_TEXT = "image_to_text"
    CHAT = "chat"
    REASONING = "reasoning"
    COMPLIANCE = "compliance"
    
class ModelProviders(Enum):
    OPENROUTER = {"base_url": "https://api.openrouter.com/v1/chat/completions/", "api_key": OPENROUTER_API_KEY}
    GROQ = {"base_url": "https://api.groq.com/openai/v1/chat/completions", "api_key": GROQ_API_KEY}
    OPENAI = {"base_url": "https://api.openai.com/v1/chat/completions/", "api_key": OPENAI_API_KEY}
    
class ModelConfig(BaseModel):
    temperature: float = Field(default=0.9, description="The temperature of the model, which controls the randomness of the output.")
    provider: str = Field(default="openai", description="The provider of the AI model.")
    base_url: str = ModelProviders.GROQ.value["base_url"]
    api_key: str = ModelProviders.GROQ.value["api_key"]
    context_space: Optional[Literal["default", "large", "small"]] = "default"
    parameter_space: Optional[Literal["default", "large", "small"]] = "default"
    purpose: Optional[Literal["default", "chat", "completion", "embedding"]] = "default"
    

models_settings: dict = {
    "default": ModelConfig(),
    "gpt-4o-mini": ModelConfig(
        provider="openai",
        **ModelProviders.OPENAI.value,
    ),
    "meta-llama/llama-3.3-70b-instruct:free": ModelConfig(provider="meta"),
    "gemini-2.3-gemma": ModelConfig(provider="google"),
}

roles_model_settings: dict = {
    Roles.BRAIN: ModelConfig(
        context_space="large",
        parameter_space="large",
    ),
    Roles.IMAGE_TO_TEXT: ModelConfig(
        context_space="default",
        parameter_space="small",
    ),
    Roles.COMPLIANCE: ModelConfig(
        provider="anthropic",
    )
}