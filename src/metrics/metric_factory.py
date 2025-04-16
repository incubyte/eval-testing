from typing import Dict, Any, List, Optional

from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    ContextualRelevancyMetric,
    ContextualRecallMetric,
    ContextualPrecisionMetric,
    ToolCorrectnessMetric,
    GEval,
    DAGMetric,
    BaseMetric
)
from deepeval.test_case import LLMTestCaseParams


class MetricFactory:
    """
    Factory class for creating metric instances.
    """
    
    @classmethod
    def create_metric(cls, metric_type: str, **kwargs) -> BaseMetric:
        """
        Create a metric instance.
        
        Args:
            metric_type: The type of metric to create
            **kwargs: Arguments to pass to the metric constructor
            
        Returns:
            BaseMetric: An instance of the requested metric
            
        Raises:
            ValueError: If the metric type is not supported
        """
        threshold = kwargs.get("threshold", 0.5)
        
        if metric_type == "answer_relevancy":
            return AnswerRelevancyMetric(threshold=threshold)
        
        elif metric_type == "faithfulness":
            return FaithfulnessMetric(threshold=threshold)
        
        elif metric_type == "contextual_relevancy":
            return ContextualRelevancyMetric(threshold=threshold)
        
        elif metric_type == "contextual_recall":
            return ContextualRecallMetric(threshold=threshold)
        
        elif metric_type == "contextual_precision":
            return ContextualPrecisionMetric(threshold=threshold)
        
        elif metric_type == "tool_correctness":
            return ToolCorrectnessMetric(threshold=threshold)
        
        elif metric_type == "custom":
            name = kwargs.get("name", "Custom Metric")
            criteria = kwargs.get("criteria", "Determine if the 'actual output' is correct.")
            evaluation_params = kwargs.get("evaluation_params", 
                                         [LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.EXPECTED_OUTPUT])
            
            return GEval(
                name=name,
                criteria=criteria,
                evaluation_params=evaluation_params,
                threshold=threshold
            )
        
        else:
            raise ValueError(f"Unknown metric type: {metric_type}")
    
    @classmethod
    def create_metrics(cls, metric_configs: List[Dict[str, Any]]) -> List[BaseMetric]:
        """
        Create multiple metric instances based on configurations.
        
        Args:
            metric_configs: List of metric configuration dictionaries
            
        Returns:
            List of BaseMetric instances
        """
        metrics = []
        
        for config in metric_configs:
            metric_type = config.pop("type")
            metrics.append(cls.create_metric(metric_type, **config))
        
        return metrics