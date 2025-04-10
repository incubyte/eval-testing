import logging
from typing import Dict, Any
import importlib.util


class RelevanceMetric:
    """Measures relevance of responses to the original query."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the relevance metric with configuration.
        
        Args:
            config: Dictionary containing metric configuration
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.embedding_model = None
        
        # Check if using embedding similarity
        self.use_embedding_similarity = config.get('use_embedding_similarity', False)
        if self.use_embedding_similarity:
            self._initialize_embedding_model()
            
    def _initialize_embedding_model(self):
        """Initialize the embedding model if available."""
        # Check if sentence-transformers is available
        if importlib.util.find_spec("sentence_transformers") is not None:
            try:
                from sentence_transformers import SentenceTransformer
                model_name = self.config.get('embedding_model', 'all-MiniLM-L6-v2')
                self.logger.info(f"Loading embedding model: {model_name}")
                self.embedding_model = SentenceTransformer(model_name)
            except ImportError:
                self.logger.warning("Failed to import sentence-transformers, falling back to keyword matching")
                self.use_embedding_similarity = False
        else:
            self.logger.warning("sentence-transformers not available, falling back to keyword matching")
            self.use_embedding_similarity = False

    def calculate(self, response: Dict[str, Any], ground_truth: str, test_case: Dict[str, Any]) -> float:
        """
        Calculate relevance score using embedding similarity or keyword matching.
        
        Args:
            response: Dictionary containing the service response
            ground_truth: String containing the expected correct answer
            test_case: Dictionary containing the test case data
            
        Returns:
            Float between 0 and 1 representing relevance score
        """
        # Extract response text
        response_text = response.get('text', '')
        if not response_text and 'answer' in response:
            response_text = response.get('answer', '')
            
        if not response_text:
            self.logger.warning(f"Empty response for test case {test_case.get('id', 'unknown')}")
            return 0.0
            
        question = test_case.get('question', '')
        if not question:
            self.logger.warning(f"Missing question for test case {test_case.get('id', 'unknown')}")
            return 0.0
            
        # Use embedding similarity if available
        if self.use_embedding_similarity and self.embedding_model is not None:
            try:
                # Encode question and response
                question_embedding = self.embedding_model.encode(question)
                response_embedding = self.embedding_model.encode(response_text)
                
                # Calculate cosine similarity
                from numpy import dot
                from numpy.linalg import norm
                similarity = dot(question_embedding, response_embedding) / (norm(question_embedding) * norm(response_embedding))
                
                return max(0.0, min(1.0, float(similarity)))
            except Exception as e:
                self.logger.warning(f"Embedding similarity calculation failed: {str(e)}")
                
        # Fallback to keyword matching
        keywords = self._extract_keywords(question)
        if not keywords:
            return 0.5  # Neutral score if no keywords found
            
        # Count how many keywords appear in the response
        response_lower = response_text.lower()
        matches = sum(1 for keyword in keywords if keyword.lower() in response_lower)
        
        # Calculate relevance score
        if len(keywords) > 0:
            return min(1.0, matches / len(keywords))
        else:
            return 0.5
            
    def _extract_keywords(self, text: str) -> list:
        """
        Extract important keywords from text.
        
        Args:
            text: String to extract keywords from
            
        Returns:
            List of keyword strings
        """
        # Simple keyword extraction by removing stopwords
        stopwords = set(['the', 'a', 'an', 'in', 'on', 'at', 'of', 'to', 'for', 'with', 'by', 'about', 'and', 'or', 'is', 'are', 'was', 'were'])
        words = text.split()
        
        # Filter out stopwords and short words
        keywords = [word for word in words if word.lower() not in stopwords and len(word) > 2]
        
        return keywords