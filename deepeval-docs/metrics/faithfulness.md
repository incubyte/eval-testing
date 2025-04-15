# Faithfulness Metric

The faithfulness metric uses LLM-as-a-judge to measure the quality of your RAG pipeline's generator by evaluating whether the `actual_output` factually aligns with the contents of your `retrieval_context`. DeepEval's faithfulness metric is a self-explaining LLM-Eval, meaning it outputs a reason for its metric score.

Although similar to the `HallucinationMetric`, the faithfulness metric in DeepEval is more concerned with contradictions between the `actual_output` and `retrieval_context` in RAG pipelines, rather than hallucination in the actual LLM itself.

## Required Arguments

To use the `FaithfulnessMetric`, you'll have to provide the following arguments when creating an `LLMTestCase`:

- `input`
- `actual_output`
- `retrieval_context`

The `input` and `actual_output` are required to create an `LLMTestCase` (and hence required by all metrics) even though they might not be used for metric calculation.

## Example

```python
from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import FaithfulnessMetric

# Replace this with the actual output from your LLM application
actual_output = "We offer a 30-day full refund at no extra cost."

# Replace this with the actual retrieved context from your RAG pipeline
retrieval_context = ["All customers are eligible for a 30 day full refund at no extra cost."]

metric = FaithfulnessMetric(
    threshold=0.7,
    model="gpt-4",
    include_reason=True
)

test_case = LLMTestCase(
    input="What if these shoes don't fit?",
    actual_output=actual_output,
    retrieval_context=retrieval_context
)

# To run metric as a standalone
# metric.measure(test_case)
# print(metric.score, metric.reason)

evaluate(test_cases=[test_case], metrics=[metric])
```

There are **EIGHT** optional parameters when creating a `FaithfulnessMetric`:

- [Optional] `threshold`: a float representing the minimum passing threshold, defaulted to 0.5.
- [Optional] `model`: a string specifying which of OpenAI's GPT models to use, **OR** any custom LLM model of type `DeepEvalBaseLLM`. Defaulted to 'gpt-4o'.
- [Optional] `include_reason`: a boolean which when set to `True`, will include a reason for its evaluation score. Defaulted to `True`.
- [Optional] `strict_mode`: a boolean which when set to `True`, enforces a binary metric score: 1 for perfection, 0 otherwise. It also overrides the current threshold and sets it to 1. Defaulted to `False`.
- [Optional] `async_mode`: a boolean which when set to `True`, enables concurrent execution within the `measure()` method. Defaulted to `True`.
- [Optional] `verbose_mode`: a boolean which when set to `True`, prints the intermediate steps used to calculate said metric to the console. Defaulted to `False`.
- [Optional] `truths_extraction_limit`: an int which when set, determines the maximum number of factual truths to extract from the `retrieval_context`. The truths extracted will be used to determine the degree of factual alignment, and will be ordered by importance, decided by your evaluation `model`. Defaulted to `None`.
- [Optional] `evaluation_template`: a class of type `FaithfulnessTemplate`, which allows you to override the default prompts used to compute the `FaithfulnessMetric` score. Defaulted to `deepeval`'s `FaithfulnessTemplate`.

## How Is It Calculated?

The `FaithfulnessMetric` score is calculated according to the following equation:

Faithfulness = Number of Truthful Claims / Total Number of Claims

The `FaithfulnessMetric` first uses an LLM to extract all claims made in the `actual_output`, before using the same LLM to classify whether each claim is truthful based on the facts presented in the `retrieval_context`.

**A claim is considered truthful if it does not contradict any facts** presented in the `retrieval_context`.

Sometimes, you may want to only consider the most important factual truths in the `retrieval_context`. If this is the case, you can choose to set the `truths_extraction_limit` parameter to limit the maximum number of truths to consider during evaluation.

## Customize Your Template

Since DeepEval's `FaithfulnessMetric` is evaluated by LLM-as-a-judge, you can likely improve your metric accuracy by overriding DeepEval's default prompt templates. This is especially helpful if:

- You're using a custom evaluation LLM, especially for smaller models that have weaker instruction following capabilities.
- You want to customize the examples used in the default `FaithfulnessTemplate` to better align with your expectations.

Here's a quick example of how you can override the process of extracting claims in the `FaithfulnessMetric` algorithm:

```python
from deepeval.metrics import FaithfulnessMetric
from deepeval.metrics.faithfulness import FaithfulnessTemplate

# Define custom template
class CustomTemplate(FaithfulnessTemplate):
    @staticmethod
    def generate_claims(actual_output: str):
        return f"""Based on the given text, please extract a comprehensive list of facts that can inferred from the provided text.
Example:
Example Text:
"CNN claims that the sun is 3 times smaller than earth."
Example JSON:
{{
    "claims": []
}}
===== END OF EXAMPLE ======
Text:
{actual_output}
JSON:"""

# Inject custom template to metric
metric = FaithfulnessMetric(evaluation_template=CustomTemplate)
metric.measure(...)
```
