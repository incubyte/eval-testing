import os
import argparse
import json
import yaml
import datetime
from dotenv import load_dotenv

from src.synthesizer import DatasetGenerator
from src.utils import ResultHandler

# Load environment variables
load_dotenv()

def generate_test_id(topic, index):
    """Generate a unique ID for test cases based on topic and index"""
    prefix = ''.join([word[0] for word in topic.lower().split()[:2]])
    return f"{prefix}-{index:03d}"

def convert_to_test_case_format(goldens, topic):
    """Convert DeepEval goldens to our test case format with metadata"""
    test_cases = []
    for i, golden in enumerate(goldens):
        # Make sure we have expected outputs - DeepEval sometimes doesn't generate them
        expected_output = None
        if hasattr(golden, "expected_output") and golden.expected_output:
            expected_output = golden.expected_output
        else:
            # Create a placeholder expected output that can be edited manually
            expected_output = f"[Sample response for: {golden.input}]\n\nThis is a placeholder response that should be edited manually."
            
        test_case = {
            "id": generate_test_id(topic, i+1),
            "input": golden.input,
            "expected_output": expected_output,
            "context": golden.context if hasattr(golden, "context") and golden.context else None,
            "metadata": {
                "category": topic.lower().replace(" ", "_"),
                "difficulty": "medium",
                "last_reviewed": datetime.datetime.now().strftime("%Y-%m-%d"),
                "reviewed_by": "auto_generated"
            }
        }
        test_cases.append(test_case)
    return test_cases

def generate_default_config(topic, test_case_path):
    """Generate a default configuration file for the test cases"""
    sanitized_topic = topic.lower().replace(" ", "_")
    config = {
        "test_suites": [
            {
                "name": f"{sanitized_topic}_eval",
                "description": f"Evaluates LLM responses to {topic} queries",
                "metrics": [
                    {
                        "type": "answer_relevancy",
                        "threshold": 0.7
                    },
                    {
                        "type": "faithfulness", 
                        "threshold": 0.8
                    },
                    {
                        "type": "custom",
                        "name": "Completeness",
                        "criteria": f"Determine if the response completely addresses the {topic} question.",
                        "threshold": 0.8
                    }
                ],
                "model_config": {
                    "provider": "openai",
                    "model_name": "gpt-4",
                    "parameters": {
                        "temperature": 0.1,
                        "max_tokens": 600
                    }
                },
                "test_cases": {
                    "source": "file",
                    "path": test_case_path
                },
                "human_review_required": True,
                "review_assignment": "review_team@example.com"
            }
        ],
        "output_dir": "results"
    }
    return config

def main():
    # Set up required environment variables for the example
    if not os.environ.get("OPENAI_API_KEY"):
        print("Please set the OPENAI_API_KEY environment variable.")
        return
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Generate synthetic evaluation datasets")
    parser.add_argument("--method", choices=["docs", "contexts", "scratch"], required=True,
                       help="Method for generating datasets: from documents, contexts, or scratch")
    parser.add_argument("--output", default="test_cases",
                       help="Output directory for the generated dataset (default: test_cases)")
    parser.add_argument("--count", type=int, default=10,
                       help="Number of test cases to generate (default: 10)")
    parser.add_argument("--topic", 
                       help="Topic for generating test cases from scratch")
    parser.add_argument("--docs", nargs="+",
                       help="Paths to document files for generating test cases")
    parser.add_argument("--contexts", nargs="+",
                       help="Context strings for generating test cases")
    parser.add_argument("--generate-config", action="store_true",
                       help="Generate default configuration YAML file in the config directory that can be edited later")
    
    args = parser.parse_args()
    
    # Create dataset generator
    dataset_generator = DatasetGenerator()
    
    # Generate dataset based on method
    if args.method == "docs":
        if not args.docs:
            print("Error: --docs argument is required for docs method")
            return
        
        topic = args.topic or os.path.basename(args.docs[0]).split('.')[0]
        print(f"Generating {args.count} test cases from {len(args.docs)} documents...")
        dataset = dataset_generator.generate_from_docs(
            document_paths=args.docs,
            num_test_cases=args.count
        )
    
    elif args.method == "contexts":
        if not args.contexts:
            print("Error: --contexts argument is required for contexts method")
            return
        
        topic = args.topic or "context_based"
        print(f"Generating {args.count} test cases from {len(args.contexts)} contexts...")
        dataset = dataset_generator.generate_from_contexts(
            contexts=args.contexts,
            num_test_cases=args.count
        )
    
    elif args.method == "scratch":
        if not args.topic:
            print("Error: --topic argument is required for scratch method")
            return
        
        topic = args.topic
        print(f"Generating {args.count} test cases for topic '{args.topic}'...")
        dataset = dataset_generator.generate_from_scratch(
            topic=args.topic,
            num_test_cases=args.count
        )
    
    # Convert goldens to our test case format
    test_cases = convert_to_test_case_format(dataset.goldens, topic)
    
    # Create the output filename based on sanitized topic
    sanitized_topic = topic.lower().replace(" ", "_")
    filename = f"{sanitized_topic}.json"
    
    # Save test cases
    os.makedirs(args.output, exist_ok=True)
    test_case_path = os.path.join(args.output, filename)
    
    # Save the test cases to a JSON file
    with open(test_case_path, 'w') as f:
        json.dump(test_cases, f, indent=2)
    
    print(f"\nGenerated {len(test_cases)} test cases")
    print(f"Test cases saved to: {test_case_path}")
    
    # Generate and save configuration file if requested
    if args.generate_config:
        config_dir = "config"
        os.makedirs(config_dir, exist_ok=True)
        config_path = os.path.join(config_dir, f"{sanitized_topic}_config.yaml")
        
        # Generate the default configuration
        config = generate_default_config(topic, test_case_path)
        
        # Save the configuration to a YAML file
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        
        print(f"Default configuration saved to: {config_path}")


if __name__ == "__main__":
    main()