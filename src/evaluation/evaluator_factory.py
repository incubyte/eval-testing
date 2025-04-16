from typing import Dict, Any

from .base_evaluator import BaseEvaluator
from .deepeval_evaluator import DeepEvalEvaluator


class EvaluatorFactory:
    """
    Factory class for creating evaluator instances.
    """
    
    _evaluators = {
        "deepeval": DeepEvalEvaluator
    }
    
    @classmethod
    def register_evaluator(cls, name: str, evaluator_class: type):
        """
        Register a new evaluator implementation.
        
        Args:
            name: The name to register the evaluator under
            evaluator_class: The evaluator class to register
        """
        if not issubclass(evaluator_class, BaseEvaluator):
            raise TypeError(f"Evaluator class must inherit from BaseEvaluator")
        
        cls._evaluators[name] = evaluator_class
    
    @classmethod
    def create_evaluator(cls, evaluator_type: str, **kwargs) -> BaseEvaluator:
        """
        Create an evaluator instance.
        
        Args:
            evaluator_type: The type of evaluator to create
            **kwargs: Arguments to pass to the evaluator constructor
            
        Returns:
            BaseEvaluator: An instance of the requested evaluator
            
        Raises:
            ValueError: If the evaluator type is not registered
        """
        if evaluator_type not in cls._evaluators:
            raise ValueError(f"Unknown evaluator type: {evaluator_type}. Available types: {list(cls._evaluators.keys())}")
        
        return cls._evaluators[evaluator_type](**kwargs)