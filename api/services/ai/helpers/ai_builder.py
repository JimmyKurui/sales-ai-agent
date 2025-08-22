from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from api.config.settings import Roles, models_settings, roles_model_settings, ModelProviders
from pydantic import HttpUrl

class AIBuilder:
    """ Class to handle AI model and provider switching, and rate limiting. """
    
    def __init__(self, model_name: str, role: Roles):
        self.model_name = model_name
        self.role = role
        self.model = self._set_model(model_name, roles_model_settings.get(role, {}))
    
    def __call__(self):
        return self.model
    
    def __str__(self):
        return f"Model using {self.model_name} acting as {self.role})"
    
    def _set_model(self, model_name, _config: dict = {}) -> dict:
        """ Set the model configuration based on the provided model name and return model configuration. """
        # if model_name not in models_settings:
            # model_name = "default"
            # raise ValueError(f"Model {model_name} is not supported.")
        
        model_settings = models_settings["default"]
        print("Model settings: ",model_settings)
        updated_settings = {
            **model_settings.model_dump(),
            **_config,
            "model": model_name
        }
        unused_fields = ("provider", "context_space", "parameter_space", "purpose")
        updated_settings = {k: v for k, v in updated_settings.items() if k not in unused_fields}
        if model_settings.base_url == ModelProviders.GROQ.value["base_url"]:
            updated_settings.pop("base_url", None)
            return ChatGroq(**updated_settings)
        else:
            return ChatOpenAI(**updated_settings)
        
    def get_model_settings(self, model_name: str) -> dict:
        """ Get the current model settings. """
        if model_name not in models_settings:
            raise ValueError(f"Model {model_name} is not supported.")
        return models_settings[model_name]
    
    def switch_model(self, new_model_name: str) -> str:
        """ Switch the model based on the role and return a model name. """
        try:
            return self._set_model(new_model_name, roles_model_settings.get(self.role, {}))
        except ValueError as e:
            raise ValueError(f"Failed to switch model: {e}") from e

    # Implement middleware based on rate limits in another file
    def switch_provider(self, provider: HttpUrl) -> str:
        """ Switch the provider for a given model and return the updated model name. """
        