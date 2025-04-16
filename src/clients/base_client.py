from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseClient(ABC):
    """
    Abstract base class for LLM clients.
    
    This class defines the interface that all client implementations must follow
    to provide a consistent way to interact with different LLM providers.
    """
    
    @abstractmethod
    def chat(self, user_input: str, **kwargs) -> Dict[str, Any]:
        """
        Send a chat message to the LLM and get a response.
        
        Args:
            user_input: The user's input message
            **kwargs: Additional arguments specific to the client implementation
            
        Returns:
            Dict containing the response details
        """
        pass
    
    @abstractmethod
    def get_conversation_history(self, conversation_id: str) -> list:
        """
        Retrieve the history of a conversation.
        
        Args:
            conversation_id: The ID of the conversation to retrieve
            
        Returns:
            List of conversation messages
        """
        pass
    
    @abstractmethod
    def create_conversation(self, title: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Create a new conversation.
        
        Args:
            title: Optional title for the conversation
            **kwargs: Additional arguments specific to the client implementation
            
        Returns:
            Dict containing the created conversation details
        """
        pass