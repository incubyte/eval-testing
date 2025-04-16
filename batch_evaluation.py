import os
import json
from dotenv import load_dotenv

from src.clients import ClientFactory
from src.evaluation import EvaluatorFactory
from src.metrics import MetricFactory
from src.utils import ResultHandler

# Load environment variables
load_dotenv()

def load_test_cases(file_path):
    """Load test cases from a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def main():
    # Set up required environment variables for the example
    if not os.environ.get("OPENAI_API_KEY"):
        print("Please set the OPENAI_API_KEY environment variable.")
        return
    
    if not os.environ.get("ROLAI_BASE_URL") or \
       not os.environ.get("ROLAI_ORGANIZATION_ID") or \
       not os.environ.get("ROLAI_AUTH_TOKEN"):
        print("Please set ROLAI_BASE_URL, ROLAI_ORGANIZATION_ID, and ROLAI_AUTH_TOKEN environment variables.")
        return
    
    # Create Rolai client
    client = ClientFactory.create_client(
        "rolai",
        base_url=os.environ["ROLAI_BASE_URL"],
        organization_id=os.environ["ROLAI_ORGANIZATION_ID"],
        auth_token=os.environ["ROLAI_AUTH_TOKEN"]
    )
    
    # Create evaluator
    evaluator = EvaluatorFactory.create_evaluator("deepeval")
    
    # Create metrics
    metrics = MetricFactory.create_metrics([
        {"type": "answer_relevancy", "threshold": 0.7},
        {"type": "custom", "name": "Correctness", "criteria": "Determine if the response is factually correct and answers the user's question completely.", "threshold": 0.7}
    ])
    
    # Sample test inputs and expected outputs
    test_cases_data = [
        {
            "input": "What is machine learning and how is it used in business?",
            "expected_output": """
            Machine learning is a branch of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. In business, it's used for:
            1. Customer segmentation and personalization
            2. Predictive analytics and forecasting
            3. Process automation
            4. Fraud detection
            5. Customer service (chatbots and virtual assistants)
            6. Supply chain optimization
            7. Quality control and predictive maintenance
            """
        },
        {
            "input": "Explain the difference between supervised and unsupervised learning.",
            "expected_output": """
            Supervised learning uses labeled training data with known outputs to learn patterns and make predictions. Examples include classification and regression.
            
            Unsupervised learning works with unlabeled data to find hidden patterns and structures without predefined outputs. Examples include clustering and dimensionality reduction.
            
            Key differences:
            - Supervised requires labeled data; unsupervised uses unlabeled data
            - Supervised has defined correct answers; unsupervised discovers patterns autonomously
            - Supervised predicts specific outcomes; unsupervised finds structure in data
            """
        },
        {
            "input": "How does natural language processing work?",
            "expected_output": """
            Natural Language Processing (NLP) works through several key steps:
            
            1. Text preprocessing: Tokenization, normalization, and removing noise
            2. Syntactic analysis: POS tagging, parsing to understand grammar structure
            3. Semantic analysis: Extracting meaning from words and sentences
            4. Pragmatic analysis: Understanding context and intent
            
            Modern NLP uses deep learning models like transformers (BERT, GPT) that learn language patterns from massive datasets. These models process text as numerical representations (embeddings) to capture semantic relationships.
            
            NLP enables applications like machine translation, sentiment analysis, chatbots, and text summarization.
            """
        },
        {
            "input": "What are neural networks and why are they important for AI?",
            "expected_output": """
            Neural networks are computational models inspired by the human brain's structure. They consist of interconnected nodes (neurons) organized in layers that process information. Each connection has a weight that adjusts during learning.
            
            They're important for AI because they:
            1. Can learn complex patterns from data without explicit programming
            2. Excel at processing unstructured data (images, text, audio)
            3. Power breakthroughs in computer vision, NLP, and reinforcement learning
            4. Enable deep learning, which has dramatically improved AI capabilities
            5. Can generalize from examples to handle new, unseen situations
            6. Scale effectively with more data and computational resources
            
            Neural networks form the foundation of most modern AI systems, enabling human-like processing capabilities.
            """
        }
    ]
    
    # Get responses from Rolai API and create test cases
    test_cases = []
    print("Generating test cases...")
    
    for i, test_data in enumerate(test_cases_data):
        print(f"Processing test case {i+1}/{len(test_cases_data)}...")
        
        response = client.chat(
            user_input=test_data["input"],
            model_name="gpt-4",
            provider="openai"
        )
        
        actual_output = response["data"]
        
        test_case = evaluator.create_test_case(
            input_text=test_data["input"],
            actual_output=actual_output,
            expected_output=test_data["expected_output"],
            name=f"Test Case {i+1}"
        )
        
        test_cases.append(test_case)
    
    # Batch evaluate test cases
    print("\nEvaluating test cases...")
    evaluation_results = evaluator.batch_evaluate(test_cases, metrics)
    
    # Print summary
    print("\n--- Evaluation Summary ---")
    for i, result in enumerate(evaluation_results):
        print(f"Test Case {i+1}: {test_cases_data[i]['input']}")
        
        for metric_name, metric_result in result["metrics"].items():
            status = "PASSED" if metric_result["passed"] else "FAILED"
            print(f"  - {metric_name}: {metric_result['score']:.2f} - {status}")
        
        print()
    
    # Save results
    output_file = ResultHandler.save_results(
        evaluation_results,
        output_dir="results"
    )
    
    print(f"Results saved to: {output_file}")


if __name__ == "__main__":
    main()