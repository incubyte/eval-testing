from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union

from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval.metrics import BaseMetric


class BaseEvaluator(ABC):
    """
    Abstract base class for evaluators.
    
    This class defines the interface that all evaluator implementations must follow
    to provide a consistent way to evaluate LLM outputs.
    """
    
    @abstractmethod
    def create_test_case(self, input_text: str, actual_output: str, **kwargs) -> LLMTestCase:
        """
        Create a test case for evaluation.
        
        Args:
            input_text: The input text
            actual_output: The actual output from the LLM
            **kwargs: Additional arguments specific to the evaluator implementation
            
        Returns:
            LLMTestCase: A test case object
        """
        pass
    
    @abstractmethod
    def evaluate(self, test_case: LLMTestCase, metrics: List[BaseMetric]) -> Dict[str, Any]:
        """
        Evaluate a test case using specified metrics.
        
        Args:
            test_case: The test case to evaluate
            metrics: List of metrics to use for evaluation
            
        Returns:
            Dict containing evaluation results
        """
        pass
    
    @abstractmethod
    def batch_evaluate(self, test_cases: List[LLMTestCase], metrics: List[BaseMetric]) -> List[Dict[str, Any]]:
        """
        Evaluate multiple test cases using specified metrics.
        
        Args:
            test_cases: The test cases to evaluate
            metrics: List of metrics to use for evaluation
            
        Returns:
            List of dicts containing evaluation results for each test case
        """
        pass