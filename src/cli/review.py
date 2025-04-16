"""
Command-line interface for reviewing and modifying test cases.
Provides a terminal-based UI for human review.
"""
import argparse
import os
import sys
import json
import yaml
from typing import Dict, Any, List, Optional
import logging
import tempfile
import subprocess

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("llm-eval-review")

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def load_yaml_config(config_path: str) -> Dict[str, Any]:
    """Load YAML configuration file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def load_test_cases(test_cases_path: str) -> List[Dict[str, Any]]:
    """Load test cases from a JSON file."""
    with open(test_cases_path, 'r') as f:
        return json.load(f)


def save_test_cases(test_cases: List[Dict[str, Any]], test_cases_path: str) -> None:
    """Save test cases to a JSON file."""
    with open(test_cases_path, 'w') as f:
        json.dump(test_cases, f, indent=2)


def open_editor(content: str) -> str:
    """Open content in the user's preferred editor and return the edited content."""
    editor = os.environ.get('EDITOR', 'vim')
    
    with tempfile.NamedTemporaryFile(suffix=".json", mode='w+', delete=False) as tmp:
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        subprocess.call([editor, tmp_path])
        with open(tmp_path, 'r') as f:
            edited_content = f.read()
        return edited_content
    finally:
        os.unlink(tmp_path)


def review_test_cases(config_path: str, suite_name: Optional[str] = None) -> None:
    """
    Review and modify test cases based on configuration file.
    
    Args:
        config_path: Path to configuration YAML file
        suite_name: Name of test suite to review (if None, review all suites)
    """
    # Load configuration
    config = load_yaml_config(config_path)
    
    # Get test suites to review
    if suite_name:
        test_suites = [s for s in config["test_suites"] if s["name"] == suite_name]
        if not test_suites:
            logger.error(f"Test suite '{suite_name}' not found in configuration")
            return
    else:
        test_suites = config["test_suites"]
    
    # Process each test suite
    for suite in test_suites:
        logger.info(f"Reviewing test suite: {suite['name']}")
        
        # Load test cases
        test_cases_path = suite["test_cases"]["path"]
        test_cases = load_test_cases(test_cases_path)
        logger.info(f"Loaded {len(test_cases)} test cases from {test_cases_path}")
        
        # Review each test case
        for i, test_case in enumerate(test_cases):
            print("\n" + "=" * 80)
            print(f"Test Case {i+1}/{len(test_cases)}: {test_case['id']}")
            print("-" * 80)
            print(f"Input: {test_case['input']}")
            print("-" * 80)
            print("Expected Output:")
            print(test_case['expected_output'])
            print("=" * 80)
            
            choice = input("\nOptions: [s]kip, [e]dit, [q]uit: ").lower()
            
            if choice == 'q':
                break
            elif choice == 'e':
                test_case_json = json.dumps(test_case, indent=2)
                edited_json = open_editor(test_case_json)
                try:
                    edited_test_case = json.loads(edited_json)
                    test_cases[i] = edited_test_case
                    print("Test case updated.")
                except json.JSONDecodeError:
                    print("Error: Invalid JSON. Test case not updated.")
            # Skip otherwise
        
        # Save test cases
        save_test_cases(test_cases, test_cases_path)
        logger.info(f"Saved {len(test_cases)} test cases to {test_cases_path}")


def main():
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description="Review and modify test cases")
    parser.add_argument("--config", required=True, help="Path to configuration YAML file")
    parser.add_argument("--suite", help="Name of test suite to review (if omitted, review all suites)")
    
    args = parser.parse_args()
    
    review_test_cases(args.config, args.suite)


if __name__ == "__main__":
    main()