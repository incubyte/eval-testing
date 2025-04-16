import os
from typing import Dict, Any, Optional
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_env_variable(name: str, default: Optional[str] = None) -> str:
    """
    Get an environment variable.
    
    Args:
        name: The name of the environment variable
        default: Optional default value if variable is not set
        
    Returns:
        The value of the environment variable
        
    Raises:
        ValueError: If the variable is not set and no default is provided
    """
    value = os.environ.get(name, default)
    if value is None:
        raise ValueError(f"Environment variable {name} is not set")
    return value


def load_config_file(file_path: str) -> Dict[str, Any]:
    """
    Load a configuration file.
    
    Args:
        file_path: Path to the configuration file
        
    Returns:
        Dictionary containing configuration values
        
    Raises:
        FileNotFoundError: If the file does not exist
        json.JSONDecodeError: If the file is not valid JSON
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
    
    with open(file_path, 'r') as file:
        return json.load(file)


def get_rolai_config() -> Dict[str, str]:
    """
    Get Rolai API configuration from environment variables.
    
    Returns:
        Dictionary containing Rolai API configuration
    """
    return {
        "base_url": get_env_variable("ROLAI_BASE_URL"),
        "organization_id": get_env_variable("ROLAI_ORGANIZATION_ID"),
        "auth_token": get_env_variable("ROLAI_AUTH_TOKEN")
    }


def get_openai_api_key() -> str:
    """
    Get OpenAI API key from environment variables.
    
    Returns:
        OpenAI API key
    """
    return get_env_variable("OPENAI_API_KEY")