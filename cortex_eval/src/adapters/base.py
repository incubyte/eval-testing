from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseServiceAdapter(ABC):
    """Base adapter for Cortex services."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the service adapter with configuration.
        
        Args:
            config: Dictionary containing adapter configuration
        """
        self.config = config

    @abstractmethod
    async def query(self, question: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Send a query to the service and return the response.
        
        Args:
            question: The query text to send to the service
            context: Optional context information for the query
            
        Returns:
            Dictionary containing the service response
        """
        pass