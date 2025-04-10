#!/usr/bin/env python3

import asyncio
import argparse
import yaml
import logging
import os
import sys
import json
from typing import Dict, Any, Optional

from src.core.test_executor import TestExecutor
from src.core.evaluator import ResponseEvaluator
from src.core.aggregator import ResultsAggregator
from src.adapters.chatbot import ChatbotAdapter
from src.adapters.rag import RAGAdapter
from src.dataset.loader import DatasetLoader
from src.dataset.validator import GroundTruthValidator
from src.reporting.database import ResultsDatabase
from src.reporting.dashboard import DashboardGenerator
from src.reporting.export import ResultsExporter


# Configure logging
def setup_logging(log_level=logging.INFO, log_file=None):
    """Set up logging configuration."""
    handlers = [logging.StreamHandler(sys.stdout)]
    
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        handlers.append(logging.FileHandler(log_file))
        
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )
    
    # Silence noisy libraries
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("aiohttp").setLevel(logging.WARNING)


# Load configuration
def load_config(config_path):
    """Load configuration from YAML file."""
    if not os.path.exists(config_path):
        logging.error(f"Configuration file not found: {config_path}")
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
        
    # Process environment variables in config
    def process_env_vars(item):
        if isinstance(item, str) and item.startswith("${") and item.endswith("}"):
            env_var = item[2:-1]
            return os.environ.get(env_var, "")
        elif isinstance(item, dict):
            return {k: process_env_vars(v) for k, v in item.items()}
        elif isinstance(item, list):
            return [process_env_vars(v) for v in item]
        else:
            return item
            
    return process_env_vars(config)


# Get service adapter
def get_adapter(service_type, config):
    """Get the appropriate service adapter based on service type."""
    adapters = {
        'chatbot': ChatbotAdapter,
        'rag': RAGAdapter,
        # Add other adapters as needed
    }

    adapter_class = adapters.get(service_type)
    if not adapter_class:
        raise ValueError(f"Unknown service type: {service_type}")

    return adapter_class(config)


async def run_tests(config_path, dataset_path, service_type, output_format=None, validate_only=False):
    """
    Run evaluation tests on the specified dataset and service.
    
    Args:
        config_path: Path to the configuration file
        dataset_path: Path to the test dataset file
        service_type: Type of service to test (e.g., 'chatbot', 'rag')
        output_format: Optional format to export results (e.g., 'json', 'csv', 'md')
        validate_only: If True, only validate the dataset without running tests
        
    Returns:
        Dictionary containing aggregated test results
    """
    # Load configuration
    config = load_config(config_path)
    logger = logging.getLogger(__name__)
    
    # Load and validate dataset
    loader = DatasetLoader()
    validator = GroundTruthValidator()
    
    try:
        test_cases = loader.load_dataset(dataset_path)
        valid_test_cases = validator.validate_dataset(test_cases)
        
        if validate_only:
            logger.info(f"Dataset validation complete: {len(valid_test_cases)} of {len(test_cases)} test cases are valid")
            validation_report_path = os.path.join("reports", "validation", 
                                               os.path.basename(dataset_path).replace(".json", "_validation.json"))
            os.makedirs(os.path.dirname(validation_report_path), exist_ok=True)
            validator.export_validation_report(test_cases, validation_report_path)
            logger.info(f"Validation report saved to {validation_report_path}")
            return
            
        if not valid_test_cases:
            logger.error("No valid test cases found in dataset")
            return
            
        logger.info(f"Using {len(valid_test_cases)} validated test cases")
    except Exception as e:
        logger.error(f"Error loading dataset: {str(e)}")
        return

    # Initialize components
    try:
        adapter = get_adapter(service_type, config.get('services', {}).get(service_type, {}))
        executor = TestExecutor(adapter, config.get('execution', {}))
        evaluator = ResponseEvaluator(config.get('metrics', {}))
        aggregator = ResultsAggregator(config.get('aggregation', {}))
        db = ResultsDatabase(config.get('database', {}))
        
        # Create run metadata
        run_metadata = {
            'service_type': service_type,
            'dataset_path': dataset_path,
            'timestamp': logger.handlers[0].formatter.converter(),
            'config': {
                'metrics': config.get('metrics', {}),
                'execution': config.get('execution', {})
            }
        }
    except Exception as e:
        logger.error(f"Error initializing components: {str(e)}")
        return

    # Execute tests
    try:
        logger.info(f"Executing test suite from {dataset_path} against {service_type} service")
        test_results = await executor.execute_test_suite(dataset_path)
        
        # Evaluate responses
        evaluated_results = [evaluator.evaluate_response(result) for result in test_results]
        
        # Aggregate results
        aggregated_results = aggregator.aggregate_results(evaluated_results)
        
        # Store results
        run_id = db.store_results(evaluated_results, run_metadata)
        aggregated_results['run_id'] = run_id
        db.store_aggregated_results(aggregated_results)
        
        # Generate dashboard
        dashboard = DashboardGenerator(config.get('dashboard', {}))
        dashboard_path = dashboard.generate(aggregated_results)
        dashboard.export_data_for_external_dashboard(aggregated_results)
        
        # Export results if requested
        if output_format:
            exporter = ResultsExporter()
            if output_format == 'json':
                export_path = exporter.export_to_json(aggregated_results)
            elif output_format == 'csv':
                export_path = exporter.export_to_csv(evaluated_results)
            elif output_format == 'md':
                export_path = exporter.export_summary_to_markdown(aggregated_results)
            else:
                logger.warning(f"Unknown output format: {output_format}")
                export_path = None
                
            if export_path:
                logger.info(f"Results exported to {export_path}")
        
        logger.info(f"Testing completed. Dashboard available at {dashboard_path}")
        
        # Print summary to console
        pass_rate = aggregated_results.get('overall', {}).get('pass_rate', 0) * 100
        mean_score = aggregated_results.get('overall', {}).get('mean_score', 0) * 100
        
        print("\n" + "="*50)
        print(f"EVALUATION SUMMARY - {service_type.upper()}")
        print("="*50)
        print(f"Total Tests: {aggregated_results.get('total_tests', 0)}")
        print(f"Pass Rate: {pass_rate:.1f}%")
        print(f"Mean Score: {mean_score:.1f}%")
        print("="*50 + "\n")
        
        return aggregated_results
    except Exception as e:
        logger.error(f"Error during test execution: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cortex Evaluation Framework")
    parser.add_argument("--config", default="config/config.yaml", help="Path to configuration file")
    parser.add_argument("--dataset", required=True, help="Path to test dataset file")
    parser.add_argument("--service", default="chatbot", choices=["chatbot", "rag", "voice", "translation"],
                     help="Service to test")
    parser.add_argument("--output", choices=["json", "csv", "md"], help="Output format for results")
    parser.add_argument("--validate-only", action="store_true", help="Only validate the dataset without running tests")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                     help="Logging level")
    parser.add_argument("--log-file", help="Path to log file")

    args = parser.parse_args()
    
    # Setup logging
    log_level = getattr(logging, args.log_level)
    setup_logging(log_level, args.log_file)
    
    # Run tests
    asyncio.run(run_tests(args.config, args.dataset, args.service, args.output, args.validate_only))