import logging
from typing import Dict, Any


class PerformanceMetric:
    """Measures performance characteristics of service responses."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the performance metric with configuration.
        
        Args:
            config: Dictionary containing metric configuration
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Set default response time threshold if not provided
        self.response_time_threshold_ms = config.get('response_time_threshold_ms', 1000)

    def calculate(self, response: Dict[str, Any], ground_truth: str, test_case: Dict[str, Any]) -> float:
        """
        Calculate performance score based on response time and other metrics.
        
        Args:
            response: Dictionary containing the service response
            ground_truth: String containing the expected correct answer
            test_case: Dictionary containing the test case data
            
        Returns:
            Float between 0 and 1 representing performance score
        """
        # Get response time from test result
        response_time_ms = test_case.get('response_time_ms', 0)
        
        # Calculate score as inverse ratio to threshold (faster is better)
        time_score = 1.0
        if response_time_ms > 0:
            time_score = min(1.0, self.response_time_threshold_ms / max(1, response_time_ms))
            
        # Calculate token efficiency if available
        token_score = self._calculate_token_efficiency(response, test_case)
        
        # Combine scores (weigh time more heavily by default)
        time_weight = self.config.get('time_weight', 0.7)
        token_weight = self.config.get('token_weight', 0.3)
        
        if token_score is None:
            # If token efficiency can't be calculated, use only time score
            return time_score
            
        combined_score = (time_score * time_weight) + (token_score * token_weight)
        return max(0.0, min(1.0, combined_score))
        
    def _calculate_token_efficiency(self, response: Dict[str, Any], test_case: Dict[str, Any]) -> float:
        """
        Calculate token efficiency score.
        
        Args:
            response: Dictionary containing the service response
            test_case: Dictionary containing the test case data
            
        Returns:
            Float between 0 and 1 representing token efficiency, or None if not applicable
        """
        # Check if token counts are available
        prompt_tokens = response.get('usage', {}).get('prompt_tokens')
        completion_tokens = response.get('usage', {}).get('completion_tokens')
        
        if not prompt_tokens or not completion_tokens:
            return None
            
        # Calculate token efficiency ratio
        # Lower ratio of completion tokens to prompt tokens is better
        # (indicates concise responses)
        token_ratio = completion_tokens / max(1, prompt_tokens)
        
        # Get expected token ratio from config or use default
        expected_ratio = self.config.get('expected_token_ratio', 1.5)
        
        # Calculate score: 1.0 if ratio <= expected, decreasing as ratio increases
        if token_ratio <= expected_ratio:
            return 1.0
        else:
            # Score decreases as ratio increases beyond expected
            return max(0.0, 1.0 - ((token_ratio - expected_ratio) / expected_ratio))