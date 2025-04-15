# Answer Relevancy Metric

The answer relevancy metric uses LLM-as-a-judge to measure the quality of your RAG pipeline's generator by evaluating how relevant the `actual_output` of your LLM application is compared to the provided `input`. DeepEval's answer relevancy metric is a self-explaining LLM-Eval, meaning it outputs a reason for its metric score.

## Required Arguments

To use the `AnswerRelevancyMetric`, you'll have to provide the following arguments when creating an `LLMTestCase`:

- `input`
- `actual_output`

The `input` and `actual_output` are required to create an `LLMTestCase` (and hence required by all metrics) even though they might not be used for metric calculation.

## Example

```python
from deepeval import evaluate
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase

# Replace this with the actual output from your LLM application
actual_output = "We offer a 30-day full refund at no extra cost."

metric = AnswerRelevancyMetric(
    threshold=0.7,
    model="gpt-4",
    include_reason=True
)

test_case = LLMTestCase(
    input="What if these shoes don't fit?",
    actual_output=actual_output
)

# To run metric as a standalone
# metric.measure(test_case)
# print(metric.score, metric.reason)

evaluate(test_cases=[test_case], metrics=[metric])
```

There are **SEVEN** optional parameters when creating an `AnswerRelevancyMetric`:

- [Optional] `threshold`: a float representing the minimum passing threshold, defaulted to 0.5.
- [Optional] `model`: a string specifying which of OpenAI's GPT models to use, **OR** any custom LLM model of type `DeepEvalBaseLLM`. Defaulted to 'gpt-4o'.
- [Optional] `include_reason`: a boolean which when set to `True`, will include a reason for its evaluation score. Defaulted to `True`.
- [Optional] `strict_mode`: a boolean which when set to `True`, enforces a binary metric score: 1 for perfection, 0 otherwise. It also overrides the current threshold and sets it to 1. Defaulted to `False`.
- [Optional] `async_mode`: a boolean which when set to `True`, enables concurrent execution within the `measure()` method. Defaulted to `True`.
- [Optional] `verbose_mode`: a boolean which when set to `True`, prints the intermediate steps used to calculate said metric to the console. Defaulted to `False`.
- [Optional] `evaluation_template`: a class of type `AnswerRelevancyTemplate`, which allows you to override the default prompts used to compute the `AnswerRelevancyMetric` score. Defaulted to `deepeval`'s `AnswerRelevancyTemplate`.

## How Is It Calculated?

The `AnswerRelevancyMetric` score is calculated according to the following equation:

Answer Relevancy = Number of Relevant Statements / Total Number of Statements

The `AnswerRelevancyMetric` first uses an LLM to extract all statements made in the `actual_output`, before using the same LLM to classify whether each statement is relevant to the `input`.

You can set the `verbose_mode` of **ANY** `deepeval` metric to `True` to debug the `measure()` method:

```python
metric = AnswerRelevancyMetric(verbose_mode=True)
metric.measure(test_case)
```

## Customize Your Template

Since DeepEval's `AnswerRelevancyMetric` is evaluated by LLM-as-a-judge, you can likely improve your metric accuracy by overriding DeepEval's default prompt templates. This is especially helpful if:

- You're using a custom evaluation LLM, especially for smaller models that have weaker instruction following capabilities.
- You want to customize the examples used in the default `AnswerRelevancyTemplate` to better align with your expectations.

Here's a quick example of how you can override the statement generation step of the `AnswerRelevancyMetric` algorithm:

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
