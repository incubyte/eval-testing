# Cortex Evaluation Framework

A comprehensive framework for evaluating AI responses from various Cortex services including chatbots, RAG systems, and more. The framework provides metrics for accuracy, relevance, safety, and performance.

## Features

- Test multiple AI services with the same datasets
- Flexible adapter system for different service types
- Detailed metrics for comprehensive evaluation
- Result storage and visualization
- Healthcare-specific compliance rules
- Export results in multiple formats

## Setup

1. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Configure your environment variables:

```bash
export CORTEX_API_KEY=your_api_key_here
```

## Usage

### Running Tests

Run evaluation tests against a service:

```bash
python main.py --dataset datasets/patient_inquiries.json --service chatbot
```

### Command-line Options

- `--config`: Path to configuration file (default: config/config.yaml)
- `--dataset`: Path to test dataset file (required)
- `--service`: Service to test (choices: chatbot, rag, voice, translation)
- `--output`: Output format for results (choices: json, csv, md)
- `--validate-only`: Only validate the dataset without running tests
- `--log-level`: Logging level (choices: DEBUG, INFO, WARNING, ERROR)
- `--log-file`: Path to log file

### Example

```bash
# Run tests against the chatbot service and export results as markdown
python main.py --dataset datasets/clinical_scenarios.json --service chatbot --output md
```

## Creating Test Datasets

Test datasets are JSON files with the following structure:

```json
[
  {
    "id": "unique_id",
    "category": "category_name",
    "question": "The question to ask",
    "ground_truth": "The expected correct answer",
    "context": {
      "additional_context": "value"
    }
  }
]
```

## Extending the Framework

### Adding New Service Adapters

Create a new adapter in `src/adapters/` that inherits from `BaseServiceAdapter`.

### Creating Custom Metrics

Add new metric classes in `src/metrics/` following the pattern of existing metrics.

## License

This project is licensed under the MIT License - see the LICENSE file for details.