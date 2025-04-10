# Cortex Eval Testing Framework - Development Guide

## Commands
- **Setup**: `python -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
- **Run tests**: `python main.py --config config/config.yaml --dataset datasets/patient_inquiries.json --service chatbot`
- **Run single test**: `python main.py --config config/config.yaml --dataset datasets/single_test.json --service chatbot`
- **Lint**: `ruff check .` 
- **Type check**: `mypy src/`

## Code Style Guidelines
- **Imports**: Group imports by standard lib, third-party, and local modules with a blank line between groups
- **Formatting**: 4-space indentation, 120 character line limit
- **Types**: Use type hints for all function parameters and return values
- **Naming**: 
  - Classes: `CamelCase`
  - Functions/variables: `snake_case` 
  - Constants: `UPPER_CASE`
- **Error handling**: Use try/except blocks with specific exception types
- **Documentation**: Use docstrings for all classes and functions
- **Async**: Use asyncio for API clients and service adapters
- **Testing**: Write unit tests for all modules

## Project Structure
Maintain the modular architecture with core, adapters, metrics, dataset, and reporting packages.