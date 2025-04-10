import logging
import time
import datetime
from typing import Dict, List, Any, Optional

from ..dataset.loader import DatasetLoader
from ..adapters.base import BaseServiceAdapter


class TestExecutor:
    """Executes test cases against Cortex services."""

    def __init__(self, service_adapter: BaseServiceAdapter, config: Dict[str, Any]):
        """
        Initialize the test executor.
        
        Args:
            service_adapter: The service adapter to use for queries
            config: Dictionary containing executor configuration
        """
        self.adapter = service_adapter
        self.config = config
        self.logger = logging.getLogger(__name__)

    async def execute_test_case(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a single test case and return results.
        
        Args:
            test_case: Dictionary containing the test case data
            
        Returns:
            Dictionary containing the test result
        """
        self.logger.info(f"Executing test case: {test_case['id']}")

        # Extract query from test case
        query = test_case['question']
        context = test_case.get('context', {})

        # Call service via adapter
        start_time = time.time()
        response = await self.adapter.query(query, context)
        response_time = time.time() - start_time

        # Return results
        return {
            'test_case': test_case,
            'response': response,
            'response_time_ms': response_time * 1000,
            'timestamp': datetime.datetime.now().isoformat()
        }

    async def execute_test_suite(self, dataset_path: str) -> List[Dict[str, Any]]:
        """
        Execute all test cases in a dataset.
        
        Args:
            dataset_path: Path to the dataset file
            
        Returns:
            List of test result dictionaries
        """
        loader = DatasetLoader()
        test_cases = loader.load_dataset(dataset_path)

        results = []
        for test_case in test_cases:
            result = await self.execute_test_case(test_case)
            results.append(result)

        return results