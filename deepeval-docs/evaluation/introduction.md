# Introduction to DeepEval

## Quick Summary

Evaluation refers to the process of testing your LLM application outputs, and requires the following components:

- Test cases
- Metrics
- Evaluation dataset

Here's a diagram of what an ideal evaluation workflow looks like using `deepeval`:

![Workflow Diagram](https://d2lsxfc3p6r9rv.cloudfront.net/workflow.png)

Your test cases will typically be in a single python file, and executing them will be as easy as running `deepeval test run`:

```bash
deepeval test run test_example.py
```

## Metrics

`deepeval` offers 14+ evaluation metrics, most of which are evaluated using LLMs.

```python
from deepeval.metrics import AnswerRelevancyMetric
answer_relevancy_metric = AnswerRelevancyMetric()
```

You'll need to create a test case to run `deepeval`'s metrics.

## Test Cases

In `deepeval`, a test case allows you to use evaluation metrics you have defined to unit test LLM applications.

```python
from deepeval.test_case import LLMTestCase
test_case = LLMTestCase(
  input="Who is the current president of the United States of America?",
  actual_output="Joe Biden",
  retrieval_context=["Joe Biden serves as the current president of America."]
)
```

In this example, `input` mimics an user interaction with a RAG-based LLM application, where `actual_output` is the output of your LLM application and `retrieval_context` is the retrieved nodes in your RAG pipeline. Creating a test case allows you to evaluate using `deepeval`'s default metrics:

```python
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric

answer_relevancy_metric = AnswerRelevancyMetric()
test_case = LLMTestCase(
  input="Who is the current president of the United States of America?",
  actual_output="Joe Biden",
  retrieval_context=["Joe Biden serves as the current president of America."]
)

answer_relevancy_metric.measure(test_case)
print(answer_relevancy_metric.score)
```

## Datasets

Datasets in `deepeval` is a collection of test cases. It provides a centralized interface for you to evaluate a collection of test cases using one or multiple metrics.

```python
from deepeval.test_case import LLMTestCase
from deepeval.dataset import EvaluationDataset
from deepeval.metrics import AnswerRelevancyMetric

answer_relevancy_metric = AnswerRelevancyMetric()
test_case = LLMTestCase(
  input="Who is the current president of the United States of America?",
  actual_output="Joe Biden",
  retrieval_context=["Joe Biden serves as the current president of America."]
)

dataset = EvaluationDataset(test_cases=[test_case])
dataset.evaluate([answer_relevancy_metric])
```

## Synthesizer

In `deepeval`, the `Synthesizer` allows you to generate synthetic datasets. This is especially helpful if you don't have production data or you don't have a golden dataset to evaluate with.

```python
from deepeval.synthesizer import Synthesizer
from deepeval.dataset import EvaluationDataset

synthesizer = Synthesizer()
goldens = synthesizer.generate_goldens_from_docs(document_paths=['example.txt', 'example.docx', 'example.pdf'])
dataset = EvaluationDataset(goldens=goldens)
```

## Evaluating With Pytest

`deepeval` allows you to run evaluations as if you're using Pytest via our Pytest integration. Simply create a test file:

```python
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric

dataset = EvaluationDataset(test_cases=[...])

@pytest.mark.parametrize(
    "test_case",
    dataset,
)
def test_customer_chatbot(test_case: LLMTestCase):
    answer_relevancy_metric = AnswerRelevancyMetric()
    assert_test(test_case, [answer_relevancy_metric])
```

And run the test file in the CLI:

```bash
deepeval test run test_example.py
```

### Parallelization

Evaluate each test case in parallel by providing a number to the `-n` flag to specify how many processes to use.

```bash
deepeval test run test_example.py -n 4
```

### Cache

Provide the `-c` flag (with no arguments) to read from the local `deepeval` cache instead of re-evaluating test cases on the same metrics.

```bash
deepeval test run test_example.py -c
```

## Evaluating Without Pytest

Alternately, you can use `deepeval`'s `evaluate` function. This approach avoids the CLI (if you're in a notebook environment), and allows for parallel test execution as well.

```python
from deepeval import evaluate
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.dataset import EvaluationDataset

dataset = EvaluationDataset(test_cases=[...])
answer_relevancy_metric = AnswerRelevancyMetric()
evaluate(dataset, [answer_relevancy_metric])
```
