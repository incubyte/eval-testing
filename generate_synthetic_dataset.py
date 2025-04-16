import os
import argparse
from dotenv import load_dotenv

from src.synthesizer import DatasetGenerator
from src.utils import ResultHandler

# Load environment variables
load_dotenv()

def main():
    # Set up required environment variables for the example
    if not os.environ.get("OPENAI_API_KEY"):
        print("Please set the OPENAI_API_KEY environment variable.")
        return
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Generate synthetic evaluation datasets")
    parser.add_argument("--method", choices=["docs", "contexts", "scratch"], required=True,
                       help="Method for generating datasets: from documents, contexts, or scratch")
    parser.add_argument("--output", default="datasets",
                       help="Output directory for the generated dataset (default: datasets)")
    parser.add_argument("--count", type=int, default=10,
                       help="Number of test cases to generate (default: 10)")
    parser.add_argument("--topic", 
                       help="Topic for generating test cases from scratch")
    parser.add_argument("--docs", nargs="+",
                       help="Paths to document files for generating test cases")
    parser.add_argument("--contexts", nargs="+",
                       help="Context strings for generating test cases")
    
    args = parser.parse_args()
    
    # Create dataset generator
    dataset_generator = DatasetGenerator()
    
    # Generate dataset based on method
    if args.method == "docs":
        if not args.docs:
            print("Error: --docs argument is required for docs method")
            return
        
        print(f"Generating {args.count} test cases from {len(args.docs)} documents...")
        dataset = dataset_generator.generate_from_docs(
            document_paths=args.docs,
            num_test_cases=args.count
        )
    
    elif args.method == "contexts":
        if not args.contexts:
            print("Error: --contexts argument is required for contexts method")
            return
        
        print(f"Generating {args.count} test cases from {len(args.contexts)} contexts...")
        dataset = dataset_generator.generate_from_contexts(
            contexts=args.contexts,
            num_test_cases=args.count
        )
    
    elif args.method == "scratch":
        if not args.topic:
            print("Error: --topic argument is required for scratch method")
            return
        
        print(f"Generating {args.count} test cases for topic '{args.topic}'...")
        dataset = dataset_generator.generate_from_scratch(
            topic=args.topic,
            num_test_cases=args.count
        )
    
    # Convert goldens to a serializable format
    results = []
    for golden in dataset.goldens:
        results.append({
            "input": golden.input,
            "expected_output": golden.expected_output if hasattr(golden, "expected_output") else None,
            "context": golden.context if hasattr(golden, "context") else None,
        })
    
    # Save results
    os.makedirs(args.output, exist_ok=True)
    output_file = ResultHandler.save_results(
        results,
        output_dir=args.output,
        filename=f"synthetic_dataset_{args.method}.json"
    )
    
    print(f"\nGenerated {len(results)} test cases")
    print(f"Dataset saved to: {output_file}")


if __name__ == "__main__":
    main()