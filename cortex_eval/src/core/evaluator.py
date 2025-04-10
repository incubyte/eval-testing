from typing import Dict, List, Any

from ..metrics.accuracy import AccuracyMetric
from ..metrics.relevance import RelevanceMetric
from ..metrics.safety import SafetyMetric
from ..metrics.performance import PerformanceMetric


class ResponseEvaluator:
    """Evaluates responses against ground truth and metrics."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the response evaluator with configuration.
        
        Args:
            config: Dictionary containing evaluator configuration
        """
        self.config = config
        self.metrics = {
            'accuracy': AccuracyMetric(config.get('accuracy', {})),
            'relevance': RelevanceMetric(config.get('relevance', {})),
            'safety': SafetyMetric(config.get('safety', {})),
            'performance': PerformanceMetric(config.get('performance', {}))
        }

    def evaluate_response(self, test_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate a test result against all metrics.
        
        Args:
            test_result: Dictionary containing test result data
            
        Returns:
            Dictionary containing the test result with evaluation
        """
        test_case = test_result['test_case']
        response = test_result['response']
        ground_truth = test_case['ground_truth']

        evaluation = {
            'test_id': test_case['id'],
            'metrics': {}
        }

        # Apply each metric
        for metric_name, metric in self.metrics.items():
            score = metric.calculate(response, ground_truth, test_case)
            evaluation['metrics'][metric_name] = score

        # Add overall score (weighted average based on config)
        weights = self.config.get('metric_weights', {
            'accuracy': 0.4,
            'relevance': 0.3,
            'safety': 0.2,
            'performance': 0.1
        })

        overall_score = sum(
            evaluation['metrics'][m] * weights.get(m, 0)
            for m in evaluation['metrics']
        )
        evaluation['overall_score'] = overall_score

        # Add pass/fail determination
        threshold = self.config.get('passing_threshold', 0.7)
        evaluation['passed'] = overall_score >= threshold

        return {**test_result, 'evaluation': evaluation}