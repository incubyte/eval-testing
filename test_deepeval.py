"""
Example test file for DeepEval integration with pytest.
"""

import os
import pytest
from dotenv import load_dotenv

from deepeval import assert_test
from deepeval.test_case import LLMTestCase

from src.clients import ClientFactory
from src.evaluation import EvaluatorFactory
from src.metrics import MetricFactory

# Load environment variables
load_dotenv()

# Check if required environment variables are set
pytest.importorskip("deepeval", reason="DeepEval not installed")
if not os.environ.get("OPENAI_API_KEY"):
    pytest.skip("OPENAI_API_KEY not set", allow_module_level=True)

# Create metrics to use in tests
metrics = MetricFactory.create_metrics([
    {"type": "answer_relevancy", "threshold": 0.7},
    {"type": "custom", "name": "Correctness", "criteria": "Determine if the response is factually correct and answers the user's question completely.", "threshold": 0.7}
])

# Sample test cases for a question answering system
test_cases = [
    {
        "input": "What is machine learning?",
        "expected": "Machine learning is a subset of artificial intelligence that involves the development of algorithms and statistical models that computer systems use to perform tasks without explicit instructions, relying on patterns and inference instead. It involves training a model on data and allowing it to learn from experience."
    },
    {
        "input": "What is the difference between supervised and unsupervised learning?",
        "expected": "Supervised learning involves training a model on a labeled dataset, where the model learns to map inputs to known outputs. Unsupervised learning, on the other hand, deals with unlabeled data and tries to find patterns or structure within the data without predefined outputs."
    }
]

@pytest.mark.skipif(
    not os.environ.get("ROLAI_BASE_URL") or 
    not os.environ.get("ROLAI_ORGANIZATION_ID") or 
    not os.environ.get("ROLAI_AUTH_TOKEN"),
    reason="Rolai API credentials not set"
)
def test_rolai_api():
    """Test that we can connect to the Rolai API."""
    client = ClientFactory.create_client(
        "rolai",
        base_url=os.environ["ROLAI_BASE_URL"],
        organization_id=os.environ["ROLAI_ORGANIZATION_ID"],
        auth_token=os.environ["ROLAI_AUTH_TOKEN"]
    )
    
    # Test creating a conversation
    conversation = client.create_conversation(title="Test Conversation")
    assert "id" in conversation
    
    # Test chat endpoint
    response = client.chat("Hello, how are you?", conversation_id=conversation["id"])
    assert "content" in response


@pytest.mark.parametrize("test_data", test_cases)
def test_hardcoded_responses(test_data):
    """
    Test with hardcoded responses for demonstration.
    
    In a real scenario, you would generate actual outputs from your LLM application
    using the client implementation.
    """
    # The actual response would come from your LLM application
    # This is just a placeholder
    actual_output = "Machine learning is a field of AI that uses algorithms to learn from data and make predictions."
    
    # Create the test case
    test_case = LLMTestCase(
        input=test_data["input"],
        actual_output=actual_output,
        expected_output=test_data["expected"]
    )
    
    # Assert that the test case passes all metrics
    assert_test(test_case, metrics)