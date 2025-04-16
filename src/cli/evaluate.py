"""
Command-line interface for running evaluations based on configuration files.
"""
import argparse
import os
import sys
import json
import yaml
from typing import Dict, Any, List, Optional
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("llm-eval")

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.clients import ClientFactory
from src.evaluation import EvaluatorFactory
from src.metrics import MetricFactory
from src.utils.result_handler import ResultHandler


def load_yaml_config(config_path: str) -> Dict[str, Any]:
    """Load YAML configuration file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def load_test_cases(test_cases_path: str) -> List[Dict[str, Any]]:
    """Load test cases from a JSON file."""
    with open(test_cases_path, 'r') as f:
        return json.load(f)


def run_evaluation(config_path: str, suite_name: Optional[str] = None) -> None:
    """
    Run evaluation based on configuration file.
    
    Args:
        config_path: Path to configuration YAML file
        suite_name: Name of test suite to run (if None, run all suites)
    """
    # Load configuration
    config = load_yaml_config(config_path)
    
    # Get test suites to run
    if suite_name:
        test_suites = [s for s in config["test_suites"] if s["name"] == suite_name]
        if not test_suites:
            logger.error(f"Test suite '{suite_name}' not found in configuration")
            return
    else:
        test_suites = config["test_suites"]
    
    output_dir = config.get("output_dir", "results")
    os.makedirs(output_dir, exist_ok=True)
    
    # Process each test suite
    for suite in test_suites:
        logger.info(f"Processing test suite: {suite['name']}")
        
        # Load test cases
        test_cases_path = suite["test_cases"]["path"]
        test_cases_data = load_test_cases(test_cases_path)
        logger.info(f"Loaded {len(test_cases_data)} test cases from {test_cases_path}")
        
        # Create client
        model_config = suite["model_config"]
        client = ClientFactory.create_client(
            "rolai",  # TODO: Make this configurable
            base_url=os.environ["ROLAI_BASE_URL"],
            organization_id=os.environ["ROLAI_ORGANIZATION_ID"],
            auth_token=os.environ["ROLAI_AUTH_TOKEN"]
        )
        
        # Create evaluator
        evaluator = EvaluatorFactory.create_evaluator("deepeval")
        
        # Create metrics
        metrics = MetricFactory.create_metrics(suite["metrics"])
        
        # Process test cases
        suite_test_cases = []
        for i, test_data in enumerate(test_cases_data):
            logger.info(f"Processing test case {i+1}/{len(test_cases_data)}: {test_data['id']}")
            
            # Generate response from API if needed (when running in CI/CD)
            if "actual_output" not in test_data:
                response = client.chat(
                    user_input=test_data["input"],
                    model_name=model_config["model_name"],
                    provider=model_config["provider"],
                    parameters=model_config.get("parameters", {})
                )
                actual_output = response["data"]
            else:
                actual_output = test_data["actual_output"]
            
            # Create test case
            test_case = evaluator.create_test_case(
                input_text=test_data["input"],
                actual_output=actual_output,
                expected_output=test_data["expected_output"],
                context=test_data.get("context"),
                name=test_data["id"]
            )
            
            suite_test_cases.append(test_case)
        
        # Batch evaluate test cases
        logger.info(f"Evaluating {len(suite_test_cases)} test cases")
        evaluation_results = evaluator.batch_evaluate(suite_test_cases, metrics)
        
        # Save results
        suite_output_dir = os.path.join(output_dir, suite["name"])
        output_file = ResultHandler.save_results(
            evaluation_results,
            output_dir=suite_output_dir
        )
        logger.info(f"Results saved to: {output_file}")
        
        # Print summary
        passed = 0
        failed = 0
        
        for result in evaluation_results:
            all_passed = True
            for metric_name, metric_result in result["metrics"].items():
                if not metric_result["passed"]:
                    all_passed = False
                    break
            
            if all_passed:
                passed += 1
            else:
                failed += 1
        
        logger.info(f"Summary: {passed} passed, {failed} failed")


def main():
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description="Run LLM evaluations based on configuration files")
    parser.add_argument("--config", required=True, help="Path to configuration YAML file")
    parser.add_argument("--suite", help="Name of test suite to run (if omitted, run all suites)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    run_evaluation(args.config, args.suite)


if __name__ == "__main__":
    main()