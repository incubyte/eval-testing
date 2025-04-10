import aiohttp
import logging
from typing import Dict, Any, Optional, List

from .base import BaseServiceAdapter


class RAGAdapter(BaseServiceAdapter):
    """Adapter for Cortex RAG (Retrieval Augmented Generation) service."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the RAG adapter with configuration.
        
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
        Send query to RAG service and return response with retrieved documents.
        
        Args:
            question: The question to ask the RAG system
            context: Optional context information
            
        Returns:
            Dictionary containing the RAG response and retrieved documents
            
        Raises:
            Exception: If the API call fails
        """
        payload = {
            'query': question,
            'max_results': context.get('max_results', self.config.get('max_results', 5)),
            'user_id': self.config.get('test_user_id', 'eval-tester')
        }
        
        # Add optional filters if provided in context
        if context and 'filters' in context:
            payload['filters'] = context['filters']
            
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

                    response_data = await response.json()
                    
                    # Ensure the response has the expected structure
                    if 'answer' not in response_data:
                        self.logger.warning("Response missing 'answer' field")
                        response_data['answer'] = ""
                        
                    if 'retrieved_documents' not in response_data:
                        self.logger.warning("Response missing 'retrieved_documents' field")
                        response_data['retrieved_documents'] = []
                        
                    return response_data
            except aiohttp.ClientError as e:
                self.logger.error(f"Request failed: {str(e)}")
                raise Exception(f"Request to RAG service failed: {str(e)}")