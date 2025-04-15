# Test Cases

## Quick Summary

A test case is a blueprint provided by `deepeval` to unit test LLM outputs. There are two types of test cases in `deepeval`: `LLMTestCase` and `ConversationalTestCase`.

While a `ConversationalTestCase` is a list of turns represented by `LLMTestCase`s, an `LLMTestCase` is the most prominent type of test case in `deepeval` and is based on **NINE** parameters:

- `input`
- `actual_output`
- [Optional] `expected_output`
- [Optional] `context`
- [Optional] `retrieval_context`
- [Optional] `tools_called`
- [Optional] `expected_tools`
- [Optional] `token_cost`
- [Optional] `completion_time`

Here's an example implementation of a test case:

```python
from deepeval.test_case import LLMTestCase, ToolCall
test_case = LLMTestCase(
    input="What if these shoes don't fit?",
    expected_output="You're eligible for a 30 day refund at no extra cost.",
    actual_output="We offer a 30-day full refund at no extra cost.",
    context=["All customers are eligible for a 30 day full refund at no extra cost."],
    retrieval_context=["Only shoes can be refunded."],
    tools_called=[ToolCall(name="WebSearch")]
)
```

## LLM Test Case

An `LLMTestCase` in `deepeval` can be used to unit test LLM application (which can just be an LLM itself) outputs, which includes use cases such as RAG and LLM agents. It contains the necessary information (`tools_called` for agents, `retrieval_context` for RAG, etc.) to evaluate your LLM application for a given `input`.

**Different metrics will require a different combination of `LLMTestCase` parameters, but they all require an `input` and `actual_output`** - regardless of whether they are used for evaluation for not.

### Input

The `input` mimics a user interacting with your LLM application. The input is the direct input to your prompt template, and so **SHOULD NOT CONTAIN** your prompt template.

```python
from deepeval.test_case import LLMTestCase
test_case = LLMTestCase(
    input="Why did the chicken cross the road?",
    # Replace this with your actual LLM application
    actual_output="Quite frankly, I don't want to know..."
)
```

### Actual Output

The `actual_output` is simply what your LLM application returns for a given input. This is what your users are going to interact with. Typically, you would import your LLM application (or parts of it) into your test file, and invoke it at runtime to get the actual output.

```python
# A hypothetical LLM application example
import chatbot
input = "Why did the chicken cross the road?"
test_case = LLMTestCase(
    input=input,
    actual_output=chatbot.run(input)
)
```

### Expected Output

The `expected_output` is literally what you would want the ideal output to be. Note that this parameter is **optional** depending on the metric you want to evaluate.

```python
# A hypothetical LLM application example
import chatbot
input = "Why did the chicken cross the road?"
test_case = LLMTestCase(
    input=input,
    actual_output=chatbot.run(input),
    expected_output="To get to the other side!"
)
```

### Context

The `context` is an **optional** parameter that represents additional data received by your LLM application as supplementary sources of golden truth. You can view it as the ideal segment of your knowledge base relevant to a specific input.

```python
# A hypothetical LLM application example
import chatbot
input = "Why did the chicken cross the road?"
test_case = LLMTestCase(
    input=input,
    actual_output=chatbot.run(input),
    expected_output="To get to the other side!",
    context=["The chicken wanted to cross the road."]
)
```

### Retrieval Context

The `retrieval_context` is an **optional** parameter that represents your RAG pipeline's retrieval results at runtime. By providing `retrieval_context`, you can determine how well your retriever is performing using `context` as a benchmark.

```python
# A hypothetical LLM application example
import chatbot
input = "Why did the chicken cross the road?"
test_case = LLMTestCase(
    input=input,
    actual_output=chatbot.run(input),
    expected_output="To get to the other side!",
    context=["The chicken wanted to cross the road."],
    retrieval_context=["The chicken liked the other side of the road better"]
)
```

### Tools Called

The `tools_called` parameter is an **optional** parameter that represents the tools your LLM agent actually invoked during execution. By providing `tools_called`, you can evaluate how effectively your LLM agent utilized the tools available to it.

A `ToolCall` object accepts 1 mandatory and 4 optional parameters:

- `name`: a string representing the **name** of the tool.
- [Optional] `description`: a string describing the **tool's purpose**.
- [Optional] `reasoning`: A string explaining the **agent's reasoning** to use the tool.
- [Optional] `output`: The tool's **output**, which can be of any data type.
- [Optional] `input_parameters`: A dictionary with string keys representing the **input parameters** (and respective values) passed into the tool function.

```python
# A hypothetical LLM application example
import chatbot
test_case = LLMTestCase(
    input="Why did the chicken cross the road?",
    actual_output=chatbot.run(input),
    # Replace this with the tools that were actually used
    tools_called=[
        ToolCall(
            name="Calculator Tool"
            description="A tool that calculates mathematical equations or expressions.",
            input={"user_input": "2+3"}
            output=5
        ),
        ToolCall(
            name="WebSearch Tool"
            reasoning="Knowledge base does not detail why the chicken crossed the road."
            input={"search_query": "Why did the chicken crossed the road?"}
            output="Because it wanted to, duh."
        )
    ]
)
```

## Assert A Test Case

Similar to Pytest, `deepeval` allows you to assert any test case you create by calling the `assert_test` function by running `deepeval test run` via the CLI.

**A test case passes only if all metrics passes.** Depending on the metric, a combination of `input`, `actual_output`, `expected_output`, `context`, and `retrieval_context` is used to ascertain whether their criterion have been met.

```python
# A hypothetical LLM application example
import chatbot
import deepeval
from deepeval import assert_test
from deepeval.metrics import HallucinationMetric
from deepeval.test_case import LLMTestCase

def test_assert_example():
    input = "Why did the chicken cross the road?"
    test_case = LLMTestCase(
        input=input,
        actual_output=chatbot.run(input),
        context=["The chicken wanted to cross the road."],
    )
    metric = HallucinationMetric(threshold=0.7)
    assert_test(test_case, metrics=[metric])

# Optionally log hyperparameters to pick the best hyperparameter for your LLM application
# using Confident AI. (run `deepeval login` in the CLI to login)
@deepeval.log_hyperparameters(model="gpt-4", prompt_template="...")
def hyperparameters():
    # Return a dict to log additional hyperparameters.
    # You can also return an empty dict {} if there's no additional parameters to log
    return {
        "temperature": 1,
        "chunk size": 500
    }
```

To execute the test cases, run `deepeval test run` via the CLI, which uses `deepeval`'s Pytest integration under the hood to execute these tests. You can also include an optional `-n` flag follow by a number (that determines the number of processes that will be used) to run tests in parallel.

```bash
deepeval test run test_assert_example.py -n 4
```

## Evaluate Test Cases in Bulk

`deepeval` offers an `evaluate` function to evaluate multiple test cases at once, which similar to `assert_test` but without the need for Pytest or the CLI.

```python
# A hypothetical LLM application example
import chatbot
from deepeval import evaluate
from deepeval.metrics import HallucinationMetric
from deepeval.test_case import LLMTestCase

test_case = LLMTestCase(
    input=input,
    actual_output=chatbot.run(input),
    context=["The chicken wanted to cross the road."],
)
metric = HallucinationMetric(threshold=0.7)
evaluate([test_case], [metric])
```
