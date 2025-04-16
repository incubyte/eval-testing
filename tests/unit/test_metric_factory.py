import unittest
from src.metrics import MetricFactory
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    GEval
)


class TestMetricFactory(unittest.TestCase):
    """Unit tests for the MetricFactory class."""
    
    def test_create_answer_relevancy_metric(self):
        """Test creating an answer relevancy metric."""
        metric = MetricFactory.create_metric("answer_relevancy", threshold=0.8)
        self.assertIsInstance(metric, AnswerRelevancyMetric)
        self.assertEqual(metric.threshold, 0.8)
    
    def test_create_faithfulness_metric(self):
        """Test creating a faithfulness metric."""
        metric = MetricFactory.create_metric("faithfulness", threshold=0.7)
        self.assertIsInstance(metric, FaithfulnessMetric)
        self.assertEqual(metric.threshold, 0.7)
    
    def test_create_custom_metric(self):
        """Test creating a custom metric."""
        metric = MetricFactory.create_metric(
            "custom",
            name="Test Metric",
            criteria="Test criteria",
            threshold=0.6
        )
        self.assertIsInstance(metric, GEval)
        self.assertEqual(metric.name, "Test Metric")
        self.assertEqual(metric.threshold, 0.6)
    
    def test_create_multiple_metrics(self):
        """Test creating multiple metrics."""
        configs = [
            {"type": "answer_relevancy", "threshold": 0.8},
            {"type": "faithfulness", "threshold": 0.7},
            {"type": "custom", "name": "Test", "criteria": "Test criteria", "threshold": 0.6}
        ]
        
        metrics = MetricFactory.create_metrics(configs)
        
        self.assertEqual(len(metrics), 3)
        self.assertIsInstance(metrics[0], AnswerRelevancyMetric)
        self.assertIsInstance(metrics[1], FaithfulnessMetric)
        self.assertIsInstance(metrics[2], GEval)
        self.assertEqual(metrics[2].name, "Test")
    
    def test_invalid_metric_type(self):
        """Test that creating an invalid metric type raises ValueError."""
        with self.assertRaises(ValueError):
            MetricFactory.create_metric("invalid_type")


if __name__ == "__main__":
    unittest.main()