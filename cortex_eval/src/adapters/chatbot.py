import aiohttp
import logging
from typing import Dict, Any, Optional

from .base import BaseServiceAdapter


class ChatbotAdapter(BaseServiceAdapter):
    """Adapter for Cortex Chatbot service."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the chatbot adapter with configuration.
        
        Args:
            config: Dictionary containing adapter configuration
        """
        super().__init__(config)
        self.api_url = config['api_url']
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {config['api_key']}"
        }
        self.logger = logging.getLogger(__name__)

    async def query(self, question: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Send query to chatbot service and return response.
        
        Args:
            question: The question to ask the chatbot
            context: Optional context information
            
        Returns:
            Dictionary containing the chatbot response
            
        Raises:
            Exception: If the API call fails
        """
        payload = {
            'query': question,
            'context': context or {},
            'user_id': self.config.get('test_user_id', 'eval-tester')
        }

        self.logger.debug(f"Sending request to {self.api_url}")
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=self.config.get('timeout_seconds', 30)
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"API call failed with status {response.status}: {error_text}")

                    return await response.json()
            except aiohttp.ClientError as e:
                self.logger.error(f"Request failed: {str(e)}")
                raise Exception(f"Request to chatbot service failed: {str(e)}")