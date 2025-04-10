import json
import logging
from typing import Dict, List, Any, Optional
import os


class DatasetLoader:
    """Loads and validates test datasets."""

    def __init__(self):
        """Initialize the dataset loader."""
        self.logger = logging.getLogger(__name__)

    def load_dataset(self, dataset_path: str) -> List[Dict[str, Any]]:
        """
        Load a test dataset from a JSON file.
        
        Args:
            dataset_path: Path to the dataset JSON file
            
        Returns:
            List of test case dictionaries
            
        Raises:
            FileNotFoundError: If the dataset file does not exist
            json.JSONDecodeError: If the dataset file is not valid JSON
            ValueError: If the dataset does not contain valid test cases
        """
        self.logger.info(f"Loading dataset from {dataset_path}")
        
        if not os.path.exists(dataset_path):
            self.logger.error(f"Dataset file not found: {dataset_path}")
            raise FileNotFoundError(f"Dataset file not found: {dataset_path}")
            
        try:
            with open(dataset_path, 'r', encoding='utf-8') as f:
                dataset = json.load(f)
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse dataset JSON: {str(e)}")
            raise
            
        # Validate dataset structure
        if not isinstance(dataset, list):
            self.logger.error("Dataset must be a list of test cases")
            raise ValueError("Dataset must be a list of test cases")
            
        # Validate each test case
        valid_test_cases = []
        for i, test_case in enumerate(dataset):
            try:
                validated_test_case = self._validate_test_case(test_case)
                valid_test_cases.append(validated_test_case)
            except ValueError as e:
                self.logger.warning(f"Skipping invalid test case at index {i}: {str(e)}")
                
        if not valid_test_cases:
            self.logger.error("No valid test cases found in dataset")
            raise ValueError("No valid test cases found in dataset")
            
        self.logger.info(f"Loaded {len(valid_test_cases)} valid test cases")
        return valid_test_cases
        
    def _validate_test_case(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a test case and ensure it has required fields.
        
        Args:
            test_case: Dictionary containing test case data
            
        Returns:
            Validated test case dictionary
            
        Raises:
            ValueError: If the test case is missing required fields
        """
        required_fields = ['id', 'question', 'ground_truth']
        
        for field in required_fields:
            if field not in test_case:
                raise ValueError(f"Test case missing required field: {field}")
                
        # Ensure id is a string
        if not isinstance(test_case['id'], str):
            test_case['id'] = str(test_case['id'])
            
        # Ensure context is a dictionary if present
        if 'context' in test_case and not isinstance(test_case['context'], dict):
            test_case['context'] = {}
            
        return test_case