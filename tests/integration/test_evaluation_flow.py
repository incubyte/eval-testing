import os
import unittest
import pytest
from dotenv import load_dotenv

from src.evaluation import EvaluatorFactory
from src.metrics import MetricFactory
from deepeval.test_case import LLMTestCase

# Load environment variables
load_dotenv()


@pytest.mark.skipif(
    not os.environ.get("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set"
)
class TestEvaluationFlow(unittest.TestCase):
    """Integration tests for the evaluation flow."""
    
    def setUp(self):
        """Set up test cases and metrics."""
        self.evaluator = EvaluatorFactory.create_evaluator("deepeval")
        
        self.metrics = MetricFactory.create_metrics([
            {"type": "custom", "name": "Correctness", "criteria": "Determine if the actual output is correct.", "threshold": 0.5}
        ])
        
        self.test_case = LLMTestCase(
            input="What is the capital of France?",
            actual_output="The capital of France is Paris.",
            expected_output="Paris is the capital and largest city of France."
        )
    
    def test_evaluation_workflow(self):
        """Test the full evaluation workflow."""
        # Evaluate the test case
        results = self.evaluator.evaluate(self.test_case, self.metrics)
        
        # Check that results contain the expected metric
        self.assertIn("Correctness", results)
        
        # Check that the metric result has the required fields
        metric_result = results["Correctness"]
        self.assertIn("score", metric_result)
        self.assertIn("reason", metric_result)
        self.assertIn("passed", metric_result)
        
        # Score should be a float between 0 and 1
        self.assertIsInstance(metric_result["score"], float)
        self.assertGreaterEqual(metric_result["score"], 0.0)
        self.assertLessEqual(metric_result["score"], 1.0)
    
    def test_batch_evaluation(self):
        """Test batch evaluation with multiple test cases."""
        # Create additional test case
        test_case2 = LLMTestCase(
            input="What is the tallest mountain in the world?",
            actual_output="Mount Everest is the tallest mountain in the world.",
            expected_output="Mount Everest is the Earth's highest mountain above sea level."
        )
        
        # Batch evaluate
        results = self.evaluator.batch_evaluate([self.test_case, test_case2], self.metrics)
        
        # Check results
        self.assertEqual(len(results), 2)
        self.assertIn("metrics", results[0])
        self.assertIn("metrics", results[1])
        self.assertIn("Correctness", results[0]["metrics"])
        self.assertIn("Correctness", results[1]["metrics"])


if __name__ == "__main__":
    unittest.main()