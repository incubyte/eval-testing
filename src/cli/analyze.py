"""
Analyzes evaluation results and determines if they meet the threshold.
Used in CI/CD pipelines to pass/fail builds based on evaluation results.
"""
import argparse
import os
import sys
import json
import glob
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
logger = logging.getLogger("llm-eval-analyze")


def load_json_results(file_path: str) -> Dict[str, Any]:
    """Load JSON results file."""
    with open(file_path, 'r') as f:
        return json.load(f)


def analyze_results(results_dir: str, threshold: float = 0.7) -> bool:
    """
    Analyze evaluation results and determine if they meet the threshold.
    
    Args:
        results_dir: Directory containing evaluation results
        threshold: Overall passing threshold (percentage of tests that must pass)
        
    Returns:
        True if results meet threshold, False otherwise
    """
    # Find all result files
    result_files = glob.glob(os.path.join(results_dir, "**", "*.json"), recursive=True)
    
    if not result_files:
        logger.error(f"No result files found in {results_dir}")
        return False
    
    logger.info(f"Found {len(result_files)} result files")
    
    total_test_cases = 0
    passed_test_cases = 0
    
    # Process each result file
    for result_file in result_files:
        logger.info(f"Processing result file: {result_file}")
        
        # Load results
        results = load_json_results(result_file)
        
        # Count test cases
        for result in results:
            total_test_cases += 1
            all_passed = True
            
            for metric_name, metric_result in result["metrics"].items():
                if not metric_result["passed"]:
                    logger.warning(f"Test case {result['test_case']['name']} failed metric {metric_name}: {metric_result['score']}")
                    all_passed = False
            
            if all_passed:
                passed_test_cases += 1
    
    # Calculate passing percentage
    if total_test_cases == 0:
        logger.error("No test cases found in results")
        return False
    
    passing_percentage = passed_test_cases / total_test_cases * 100
    
    logger.info(f"Total test cases: {total_test_cases}")
    logger.info(f"Passed test cases: {passed_test_cases}")
    logger.info(f"Passing percentage: {passing_percentage:.2f}%")
    logger.info(f"Threshold: {threshold * 100:.2f}%")
    
    # Check if results meet threshold
    meets_threshold = passing_percentage >= threshold * 100
    
    if meets_threshold:
        logger.info("Results meet threshold")
    else:
        logger.error("Results do not meet threshold")
    
    return meets_threshold


def main():
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description="Analyze evaluation results")
    parser.add_argument("--results", required=True, help="Directory containing evaluation results")
    parser.add_argument("--threshold", type=float, default=0.7, help="Overall passing threshold (0.0-1.0)")
    
    args = parser.parse_args()
    
    success = analyze_results(args.results, args.threshold)
    
    # Exit with appropriate exit code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()