import requests
import json
from typing import Dict, Any, Optional, List

from .base_client import BaseClient


class RolaiClient(BaseClient):
    """
    Implementation of BaseClient for Rolai API.
    """
    
    def __init__(self, base_url: str, organization_id: str, auth_token: str):
        """
        Initialize the Rolai client.
        
        Args:
            base_url: The base URL for the Rolai API
            organization_id: The ID of the organization
            auth_token: The authentication token for API requests
        """
        self.base_url = base_url
        self.organization_id = organization_id
        self.headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }
    
    def chat(self, user_input: str, **kwargs) -> Dict[str, Any]:
        """
        Send a chat message to Rolai API and get a response.
        
        Args:
            user_input: The user's input message
            **kwargs: Additional arguments including:
                - model_name: The LLM model to use
                - provider: The provider of the LLM
                - conversation_id: Optional conversation ID
                - interaction_type: Type of interaction (CHATMODEL or AGENT)
                
        Returns:
            Dict containing the response details
        """
        model_name = kwargs.get("model_name", "gpt-4")
        provider = kwargs.get("provider", "openai")
        interaction_type = kwargs.get("interaction_type", "CHATMODEL")
        
        endpoint = f"{self.base_url}/{self.organization_id}/chat"
        
        payload = {
            "userRequest": user_input,
            "interactionType": interaction_type,
            "provider": provider,
            "modelName": model_name
        }
        
        # Add conversationId if provided
        conversation_id = kwargs.get("conversation_id")
        if conversation_id:
            payload["conversationId"] = conversation_id
        
        response = requests.post(endpoint, headers=self.headers, json=payload)
        response.raise_for_status()
        
        return response.json()
    
    def get_conversation_history(self, conversation_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve the history of a conversation from Rolai API.
        
        Args:
            conversation_id: The ID of the conversation to retrieve
            
        Returns:
            List of conversation messages
        """
        endpoint = f"{self.base_url}/{self.organization_id}/chat/conversations/{conversation_id}"
        
        response = requests.get(endpoint, headers=self.headers)
        response.raise_for_status()
        
        return response.json()
    
    def create_conversation(self, title: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Create a new conversation in Rolai API.
        
        Args:
            title: Optional title for the conversation
            **kwargs: Additional arguments including:
                - model_name: The LLM model to use
                - interaction_type: Type of interaction (CHATMODEL or AGENT)
                - use_knowledge_base: Whether to use knowledge base
                - is_web_search_enabled: Whether web search is enabled
                
        Returns:
            Dict containing the created conversation details
        """
        model_name = kwargs.get("model_name", "gpt-4")
        interaction_type = kwargs.get("interaction_type", "CHATMODEL")
        use_knowledge_base = kwargs.get("use_knowledge_base", False)
        is_web_search_enabled = kwargs.get("is_web_search_enabled", False)
        
        endpoint = f"{self.base_url}/{self.organization_id}/conversations"
        
        payload = {
            "title": title or "New Conversation",
            "interactionType": interaction_type,
            "useKnowledgeBase": use_knowledge_base,
            "model": model_name,
            "isWebSearchEnabled": is_web_search_enabled,
            "isDeepResearchEnabled": False
        }
        
        response = requests.post(endpoint, headers=self.headers, json=payload)
        response.raise_for_status()
        
        return response.json()