import logging
from typing import Dict, List, Any, Optional, Set
import json
import os


class GroundTruthValidator:
    """Validates ground truth data in test cases."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the ground truth validator.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
    def validate_ground_truth(self, test_case: Dict[str, Any]) -> bool:
        """
        Validate ground truth for a test case.
        
        Args:
            test_case: Dictionary containing test case data
            
        Returns:
            True if the ground truth is valid, False otherwise
        """
        if 'ground_truth' not in test_case:
            self.logger.warning(f"Test case {test_case.get('id', 'unknown')} has no ground truth")
            return False
            
        ground_truth = test_case['ground_truth']
        
        # Check if ground truth is empty
        if not ground_truth or (isinstance(ground_truth, str) and not ground_truth.strip()):
            self.logger.warning(f"Test case {test_case.get('id', 'unknown')} has empty ground truth")
            return False
            
        # If ground truth is a list, check if it's empty
        if isinstance(ground_truth, list) and not ground_truth:
            self.logger.warning(f"Test case {test_case.get('id', 'unknown')} has empty ground truth list")
            return False
            
        return True
        
    def validate_dataset(self, dataset: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Validate all ground truths in a dataset.
        
        Args:
            dataset: List of test case dictionaries
            
        Returns:
            List of test cases with valid ground truths
        """
        valid_test_cases = []
        
        for test_case in dataset:
            if self.validate_ground_truth(test_case):
                valid_test_cases.append(test_case)
                
        self.logger.info(f"Validated {len(valid_test_cases)} of {len(dataset)} test cases")
        return valid_test_cases
        
    def export_validation_report(self, dataset: List[Dict[str, Any]], output_path: str) -> None:
        """
        Export a validation report for a dataset.
        
        Args:
            dataset: List of test case dictionaries
            output_path: Path to write the validation report
            
        Returns:
            None
        """
        validation_results = []
        
        for test_case in dataset:
            test_id = test_case.get('id', 'unknown')
            is_valid = self.validate_ground_truth(test_case)
            
            validation_results.append({
                'test_id': test_id,
                'valid': is_valid,
                'error': None if is_valid else "Invalid or missing ground truth"
            })
            
        report = {
            'total_test_cases': len(dataset),
            'valid_test_cases': sum(1 for result in validation_results if result['valid']),
            'results': validation_results
        }
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
            
        self.logger.info(f"Exported validation report to {output_path}")