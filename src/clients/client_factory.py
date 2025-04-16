from typing import Dict, Any

from .base_client import BaseClient
from .rolai_client import RolaiClient


class ClientFactory:
    """
    Factory class for creating LLM client instances.
    """
    
    _clients = {
        "rolai": RolaiClient
    }
    
    @classmethod
    def register_client(cls, name: str, client_class: type):
        """
        Register a new client implementation.
        
        Args:
            name: The name to register the client under
            client_class: The client class to register
        """
        if not issubclass(client_class, BaseClient):
            raise TypeError(f"Client class must inherit from BaseClient")
        
        cls._clients[name] = client_class
    
    @classmethod
    def create_client(cls, client_type: str, **kwargs) -> BaseClient:
        """
        Create a client instance.
        
        Args:
            client_type: The type of client to create
            **kwargs: Arguments to pass to the client constructor
            
        Returns:
            BaseClient: An instance of the requested client
            
        Raises:
            ValueError: If the client type is not registered
        """
        if client_type not in cls._clients:
            raise ValueError(f"Unknown client type: {client_type}. Available types: {list(cls._clients.keys())}")
        
        return cls._clients[client_type](**kwargs)