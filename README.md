# Evaluation Testing Framework

This framework provides a modular and extensible approach to evaluating LLM outputs using DeepEval, with support for multiple clients.

## Features

- Abstract client interface with Rolai implementation
- Extensible architecture to support additional LLM clients
- DeepEval integration for measuring output quality
- Support for multiple metrics
- Synthetic dataset generation
- Batch evaluation capabilities
- Results storage and management

## Project Structure

```
├── src/
│   ├── clients/             # LLM client implementations
│   ├── evaluation/          # Evaluation framework
│   ├── metrics/             # Metric definitions and factory
│   ├── synthesizer/         # Synthetic data generation
│   └── utils/               # Utility functions
├── tests/                   # Test cases
│   ├── unit/                # Unit tests
│   └── integration/         # Integration tests
├── simple_test_case.py      # Example of a simple test case
├── batch_evaluation.py      # Example of batch evaluation
├── generate_synthetic_dataset.py  # Example of dataset generation
├── conftest.py              # pytest configuration
└── test_deepeval.py         # Example pytest tests
```

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and update with your API keys:
   ```bash
   cp .env.example .env
   ```

## Usage

### Running a Simple Test Case

```bash
python simple_test_case.py
```

### Running Batch Evaluation

```bash
python batch_evaluation.py
```

### Production-Ready Evaluation

For production use, this framework provides a configurable CLI with support for:
- YAML configuration files
- Human review of test cases
- CI/CD integration with Azure DevOps

#### Running Evaluations with Configuration

```bash
python -m src.cli.evaluate --config config/default.yaml --suite customer_service_eval
```

#### Reviewing Test Cases

```bash
python -m src.cli.review --config config/default.yaml --suite customer_service_eval
```

#### CI/CD Integration

The framework includes Azure DevOps pipeline definitions in `azure-pipelines/llm-eval.yml` that can be used to:
1. Run evaluations as part of your CI/CD pipeline
2. Store evaluation results as build artifacts
3. Notify teams about evaluation results
4. Pass/fail builds based on evaluation thresholds

See the [CI/CD Integration Guide](docs/cicd-integration.md) for details.

### Generating Synthetic Datasets

The framework provides multiple methods for generating synthetic evaluation datasets using DeepEval's synthesizer:

```bash
# Generate from documents - creates test cases from your knowledge base documents
python generate_synthetic_dataset.py --method docs --docs path/to/doc1.pdf path/to/doc2.pdf --count 10 --output test_cases --generate-config

# Generate from contexts - creates test cases from provided context strings
python generate_synthetic_dataset.py --method contexts --contexts "Context 1" "Context 2" --count 10 --topic "My Topic" --output test_cases --generate-config

# Generate from scratch - creates test cases for a specific topic without context
python generate_synthetic_dataset.py --method scratch --topic "Machine Learning" --count 10 --output test_cases --generate-config
```

Generated test cases are saved as JSON files in the specified output directory (defaults to `test_cases/`). Each test case includes:
- Unique ID based on the topic
- Input query
- Expected output
- Optional context
- Metadata (category, difficulty, review status)

When `--generate-config` is specified, a default YAML configuration file will be created in the `config/` directory with recommended evaluation metrics and thresholds for the generated test cases.

### Running Tests with pytest

```bash
pytest test_deepeval.py -v
```

### Integration with DeepEval CLI

```bash
deepeval test run test_deepeval.py
```

## Extending the Framework

### Adding a New Client

1. Create a new client class in `src/clients/` that inherits from `BaseClient`
2. Implement all required methods
3. Register the client in `ClientFactory`

### Adding a New Evaluator

1. Create a new evaluator class in `src/evaluation/` that inherits from `BaseEvaluator`
2. Implement all required methods
3. Register the evaluator in `EvaluatorFactory`

## License

MIT
