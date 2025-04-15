# Metrics Introduction

## Quick Summary

In `deepeval`, a metric serves as a standard of measurement for evaluating the performance of an LLM output based on a specific criteria of interest. Essentially, while the metric acts as the ruler, a test case represents the thing you're trying to measure. `deepeval` offers a range of default metrics for you to quickly get started with, such as:

- G-Eval
- DAG (Deep Acyclic Graph)
- RAG:
  - Answer Relevancy
  - Faithfulness
  - Contextual Relevancy
  - Contextual Precision
  - Contextual Recall
- Agents:
  - Tool Correctness
  - Task Completion
- Others:
  - Json Correctness
  - Ragas
  - Hallucination
  - Toxicity
  - Bias
  - Summarization

`deepeval` also offers conversational metrics, which are metrics used to evaluate conversations instead of individual, granular LLM interactions. These include:

- Conversational G-Eval
- Knowledge Retention
- Role Adherence
- Conversation Completeness
- Conversation Relevancy

You can also easily develop your own custom evaluation metrics in `deepeval`. All metrics are measured on a test case.

## Types of Metrics

`deepeval` offers a wide range of **_custom_** and **_default_** metrics and all of them uses LLM-as-a-judge. There are two types of custom metrics, with varying degree of deterministicity:

- G-Eval
- DAG

The DAG metric is a decision-tree based LLM-evaluated metric, and is currently the most versitile metric `deepeval` has to offer. However, G-Eval is also extremely competent and takes no effort at all to setup so we recommend everyone to start with G-Eval and move to DAG if there's a need for it.

`deepeval` also offers **_default_** metrics, which are pre-built for different LLM systems/use cases. For example, `deepeval` offers the famous RAG metrics out-of-the-box:

- Answer Relevancy
- Faithfulness
- Contextual Relevancy
- Contextual Precision
- Contextual Recall

All of `deepeval`'s metrics output a score between 0-1. A metric is only successful if the evaluation score is equal to or greater than `threshold`, which is defaulted to `0.5` for all metrics.

## Using OpenAI

To use OpenAI for `deepeval`'s LLM-Evals (metrics evaluated using an LLM), supply your `OPENAI_API_KEY` in the CLI:

```bash
export OPENAI_API_KEY=<your-openai-api-key>
```

Alternatively, if you're working in a notebook enviornment (Jupyter or Colab), set your `OPENAI_API_KEY` in a cell:

```python
%env OPENAI_API_KEY=<your-openai-api-key>
```

### Azure OpenAI

`deepeval` also allows you to use Azure OpenAI for metrics that are evaluated using an LLM. Run the following command in the CLI to configure your `deepeval` enviornment to use Azure OpenAI for **all** LLM-based metrics.

```bash
deepeval set-azure-openai \
    --openai-endpoint=<endpoint> \ # e.g. https://example-resource.azure.openai.com/
    --openai-api-key=<api_key> \
    --openai-model-name=<model_name> \ # e.g. gpt-4o
    --deployment-name=<deployment_name> \  # e.g. Test Deployment
    --openai-api-version=<openai_api_version> \ # e.g. 2025-01-01-preview
    --model-version=<model_version> # e.g. 2024-11-20
```

## Running Evaluations With Metrics

To run evaluations using any metric of your choice, simply provide a list of test cases to evaluate your metrics against:

```python
from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric

test_case = LLMTestCase(input="...", actual_output="...")
evaluate(test_cases=[test_case], metrics=[AnswerRelevancyMetric()])
```

The `evaluate()` function or `deepeval test run` **is the best way to run evaluations**. They offer tons of features out of the box, including caching, parallelization, cost tracking, error handling, and integration with Confident AI.

## Measuring A Metric

You can also execute each metric individually. All metrics in `deepeval`, including custom metrics that you create:

- can be executed via the `metric.measure()` method
- can have its score accessed via `metric.score`, which ranges from 0 - 1
- can have its score reason accessed via `metric.reason`
- can have its status accessed via `metric.is_successful()`
- can be used to evaluate test cases or entire datasets, with or without Pytest
- has a `threshold` that acts as the threshold for success. `metric.is_successful()` is only true if `metric.score` is above/below `threshold`
- has a `strict_mode` property, which when turned on enforces `metric.score` to a binary one
- has a `verbose_mode` property, which when turned on prints metric logs whenever a metric is executed

In additional, all metrics in `deepeval` execute asynchronously by default. This behavior is something you can configure via the `async_mode` parameter when instantiating a metric.

Here's a quick example:

```python
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase

# Initialize a test case
test_case = LLMTestCase(
    input="...",
    actual_output="...",
    retrieval_context=["..."]
)

# Initialize metric with threshold
metric = AnswerRelevancyMetric(threshold=0.5)
```

Using this metric, you can either execute it directly as a standalone to get its score and reason:

```python
metric.measure(test_case)
print(metric.score)
print(metric.reason)
```

Or you can either assert a test case using `assert_test()` via `deepeval test run`:

```python
from deepeval import assert_test

def test_answer_relevancy():
    assert_test(test_case, [metric])
```

```bash
deepeval test run test_file.py
```

Or using the `evaluate` function:

```python
from deepeval import evaluate

evaluate([test_case], [metric])
```

## Debugging A Metric

You can turn on `verbose_mode` for **ANY** `deepeval` metric at metric initialization to debug a metric whenever the `measure()` or `a_measure()` method is called:

```python
metric = AnswerRelevancyMetric(verbose_mode=True)
metric.measure(test_case)
```

## Customizing Metric Prompts

All of `deepeval`'s metrics uses LLM-as-a-judge which comes with a set of default prompt templates unique to each metric that are used for evaluation. While `deepeval` has a laid out algorithm to each metric, you can still customize these prompt templates to improve the accuracy and stability of your evaluation scores. This can be done by providing a custom template class as the `evaluation_template` to your metric of choice.

Here's a quick example of how you can define a custom `AnswerRelevancyTemplate` and inject it into the `AnswerRelevancyMetric` through the `evaluation_params` parameter:

```python
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.metrics.answer_relevancy import AnswerRelevancyTemplate

# Define custom template
class CustomTemplate(AnswerRelevancyTemplate):
    @staticmethod
    def generate_statements(actual_output: str):
        return f"""Given the text, breakdown and generate a list of statements presented.
Example:
Our new laptop model features a high-resolution Retina display for crystal-clear visuals.
{{
    "statements": [
        "The new laptop model has a high-resolution Retina display."
    ]
}}
===== END OF EXAMPLE ======
Text:
{actual_output}
JSON:"""

# Inject custom template to metric
metric = AnswerRelevancyMetric(evaluation_template=CustomTemplate)
metric.measure(...)
```
