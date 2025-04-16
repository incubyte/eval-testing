from typing import Dict, Any, List, Optional, Union
import uuid

from deepeval import evaluate, assert_test
from deepeval.test_case import LLMTestCase, LLMTestCaseParams, ConversationalTestCase
from deepeval.metrics import BaseMetric
from deepeval.dataset import EvaluationDataset

from .base_evaluator import BaseEvaluator


class DeepEvalEvaluator(BaseEvaluator):
    """
    Implementation of BaseEvaluator using DeepEval.
    """
    
    def create_test_case(self, input_text: str, actual_output: str, **kwargs) -> LLMTestCase:
        """
        Create a test case for evaluation using DeepEval.
        
        Args:
            input_text: The input text
            actual_output: The actual output from the LLM
            **kwargs: Additional arguments including:
                - expected_output: The expected output
                - context: The context used for retrieval
                - retrieval_context: Alias for context
                - name: Optional name for the test case
                - conversation_history: For conversational test cases
                
        Returns:
            LLMTestCase: A test case object
        """
        # Get test case parameters
        expected_output = kwargs.get("expected_output")
        context = kwargs.get("context") or kwargs.get("retrieval_context")
        name = kwargs.get("name", f"test-{uuid.uuid4()}")
        conversation_history = kwargs.get("conversation_history")
        
        # Handle conversational test cases
        if conversation_history:
            return ConversationalTestCase(
                input=input_text,
                actual_output=actual_output,
                expected_output=expected_output,
                context=context,
                conversation_history=conversation_history,
                name=name
            )
        
        # Handle regular test cases
        return LLMTestCase(
            input=input_text,
            actual_output=actual_output,
            expected_output=expected_output,
            context=context,
            name=name
        )
    
    def evaluate(self, test_case: LLMTestCase, metrics: List[BaseMetric]) -> Dict[str, Any]:
        """
        Evaluate a test case using specified metrics with DeepEval.
        
        Args:
            test_case: The test case to evaluate
            metrics: List of metrics to use for evaluation
            
        Returns:
            Dict containing evaluation results
        """
        results = {}
        
        # Evaluate each metric individually
        for metric in metrics:
            metric.measure(test_case)
            # Use __name__ if available, otherwise use class name
            metric_name = getattr(metric, 'name', getattr(metric, '__name__', metric.__class__.__name__))
            results[metric_name] = {
                "score": metric.score,
                "reason": metric.reason,
                "passed": metric.score >= metric.threshold if hasattr(metric, "threshold") else None
            }
        
        return results
    
    def batch_evaluate(self, test_cases: List[LLMTestCase], metrics: List[BaseMetric]) -> List[Dict[str, Any]]:
        """
        Evaluate multiple test cases using specified metrics with DeepEval.
        
        Args:
            test_cases: The test cases to evaluate
            metrics: List of metrics to use for evaluation
            
        Returns:
            List of dicts containing evaluation results for each test case
        """
        # Create a dataset
        dataset = EvaluationDataset(test_cases=test_cases)
        
        # Initialize results list
        results = []
        
        # Evaluate each test case
        for test_case in test_cases:
            test_result = self.evaluate(test_case, metrics)
            
            # Add test case info to results
            result = {
                "test_case": {
                    "input": test_case.input,
                    "actual_output": test_case.actual_output,
                    "name": test_case.name if hasattr(test_case, "name") else None
                },
                "metrics": test_result
            }
            
            results.append(result)
        
        return results
    
    def run_evaluation_with_pytest(self, test_cases: List[LLMTestCase], metrics: List[BaseMetric]) -> None:
        """
        Run evaluations using pytest integration (for CLI usage).
        
        Args:
            test_cases: The test cases to evaluate
            metrics: List of metrics to use for evaluation
        """
        for test_case in test_cases:
            assert_test(test_case, metrics)