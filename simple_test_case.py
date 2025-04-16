import os
from dotenv import load_dotenv

from src.clients import ClientFactory
from src.evaluation import EvaluatorFactory
from src.metrics import MetricFactory

# Load environment variables
load_dotenv()

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

    
    # User input
    user_input = "What is machine learning and how is it used in business?"
    
    # Get response from Rolai API
    response = client.chat(
        user_input=user_input,
        model_name="gpt-4",
        provider="openai"
    )
    
    # Extract actual output
    actual_output = response["data"]
    print("\n--- LLM Response ---")
    print(actual_output)
    print("-------------------\n")
    
    # Sample expected output for the machine learning question
    expected_output = """
    Machine learning is a branch of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. In business, it's used for:
    1. Customer segmentation and personalization
    2. Predictive analytics and forecasting
    3. Process automation
    4. Fraud detection
    5. Customer service (chatbots and virtual assistants)
    6. Supply chain optimization
    7. Quality control and predictive maintenance
    """
    
    # Create test case
    test_case = evaluator.create_test_case(
        input_text=user_input,
        actual_output=actual_output,
        expected_output=expected_output
    )
    
    # Evaluate test case
    results = evaluator.evaluate(test_case, metrics)
    
    # Print results
    print("--- Evaluation Results ---")
    for result in results.items():
        print(f"{result}")
        print()
    
    print("------------------------")


if __name__ == "__main__":
    main()