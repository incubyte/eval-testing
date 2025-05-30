# Contextual Recall

  * [](/)
  * Evaluation
  * Metrics
  * Contextual Recall

On this page

# Contextual Recall

The contextual recall metric uses LLM-as-a-judge to measure the quality of your RAG pipeline's retriever by evaluating the extent of which the `retrieval_context` aligns with the `expected_output`. `deepeval`'s contextual recall metric is a self-explaining LLM-Eval, meaning it outputs a reason for its metric score.

tip

Not sure if the `ContextualRecallMetric` is suitable for your use case? Run the follow command to find out:
    
    
    deepeval recommend metrics  
    

## Required Arguments​

To use the `ContextualRecallMetric`, you'll have to provide the following arguments when creating an [`LLMTestCase`](/docs/evaluation-test-cases#llm-test-case):

  * `input`
  * `actual_output`
  * `expected_output`
  * `retrieval_context`

The `input` and `actual_output` are required to create an `LLMTestCase` (and hence required by all metrics) even though they might not be used for metric calculation. Read the How Is It Calculated section below to learn more.

## Example​
    
    
    from deepeval import evaluate  
    from deepeval.test_case import LLMTestCase  
    from deepeval.metrics import ContextualRecallMetric  
      
    # Replace this with the actual output from your LLM application  
    actual_output = "We offer a 30-day full refund at no extra cost."  
      
    # Replace this with the expected output from your RAG generator  
    expected_output = "You are eligible for a 30 day full refund at no extra cost."  
      
    # Replace this with the actual retrieved context from your RAG pipeline  
    retrieval_context = ["All customers are eligible for a 30 day full refund at no extra cost."]  
      
    metric = ContextualRecallMetric(  
        threshold=0.7,  
        model="gpt-4",  
        include_reason=True  
    )  
    test_case = LLMTestCase(  
        input="What if these shoes don't fit?",  
        actual_output=actual_output,  
        expected_output=expected_output,  
        retrieval_context=retrieval_context  
    )  
      
    # To run metric as a standalone  
    # metric.measure(test_case)  
    # print(metric.score, metric.reason)  
      
    evaluate(test_cases=[test_case], metrics=[metric])  
    

There are **SEVEN** optional parameters when creating a `ContextualRecallMetric`:

  * [Optional] `threshold`: a float representing the minimum passing threshold, defaulted to 0.5.
  * [Optional] `model`: a string specifying which of OpenAI's GPT models to use, **OR** [any custom LLM model](/docs/metrics-introduction#using-a-custom-llm) of type `DeepEvalBaseLLM`. Defaulted to 'gpt-4o'.
  * [Optional] `include_reason`: a boolean which when set to `True`, will include a reason for its evaluation score. Defaulted to `True`.
  * [Optional] `strict_mode`: a boolean which when set to `True`, enforces a binary metric score: 1 for perfection, 0 otherwise. It also overrides the current threshold and sets it to 1. Defaulted to `False`.
  * [Optional] `async_mode`: a boolean which when set to `True`, enables [concurrent execution within the `measure()` method.](/docs/metrics-introduction#measuring-metrics-in-async) Defaulted to `True`.
  * [Optional] `verbose_mode`: a boolean which when set to `True`, prints the intermediate steps used to calculate said metric to the console, as outlined in the How Is It Calculated section. Defaulted to `False`.
  * [Optional] `evaluation_template`: a class of type `ContextualRecallTemplate`, which allows you to override the default prompts used to compute the `ContextualRecallMetric` score. Defaulted to `deepeval`'s `ContextualRecallTemplate`.

### As a standalone​

You can also run the `ContextualRecallMetric` on a single test case as a standalone, one-off execution.
    
    
    ...  
      
    metric.measure(test_case)  
    print(metric.score, metric.reason)  
    

caution

This is great for debugging or if you wish to build your own evaluation pipeline, but you will **NOT** get the benefits (testing reports, Confident AI platform) and all the optimizations (speed, caching, computation) the `evaluate()` function or `deepeval test run` offers.

## How Is It Calculated?​

The `ContextualRecallMetric` score is calculated according to the following equation:

Contextual Recall=Number of Attributable StatementsTotal Number of Statements\text{Contextual Recall} = \frac{\text{Number of Attributable Statements}}{\text{Total Number of Statements}}Contextual Recall=Total Number of StatementsNumber of Attributable Statements​

The `ContextualRecallMetric` first uses an LLM to extract all **statements made in the`expected_output`**, before using the same LLM to classify whether each statement can be attributed to nodes in the `retrieval_context`.

info

We use the `expected_output` instead of the `actual_output` because we're measuring the quality of the RAG retriever for a given ideal output.

A higher contextual recall score represents a greater ability of the retrieval system to capture all relevant information from the total available relevant set within your knowledge base.

## Customize Your Template​

Since `deepeval`'s `ContextualRecallMetric` is evaluated by LLM-as-a-judge, you can likely improve your metric accuracy by [overriding `deepeval`'s default prompt templates](/docs/metrics-introduction#customizing-metric-prompts). This is especially helpful if:

  * You're using a [custom evaluation LLM](/guides/guides-using-custom-llms), especially for smaller models that have weaker instruction following capabilities.
  * You want to customize the examples used in the default `ContextualRecallTemplate` to better align with your expectations.

tip

You can learn what the default `ContextualRecallTemplate` looks like [here on GitHub](https://github.com/confident-ai/deepeval/blob/main/deepeval/metrics/contextual_recall/template.py), and should read the How Is It Calculated section above to understand how you can tailor it to your needs.

Here's a quick example of how you can override the relevancy classification step of the `ContextualRecallMetric` algorithm:
    
    
    from deepeval.metrics import ContextualRecallMetric  
    from deepeval.metrics.contextual_recall import ContextualRecallTemplate  
      
    # Define custom template  
    class CustomTemplate(ContextualRecallTemplate):  
        @staticmethod  
        def generate_verdicts(expected_output: str, retrieval_context: List[str]):  
            return f"""For EACH sentence in the given expected output below, determine whether the sentence can be attributed to the nodes of retrieval contexts.  
      
    Example JSON:  
    {{  
        "verdicts": [  
            {{  
                "verdict": "yes",  
                "reason": "..."  
            }},  
        ]  
    }}  
      
    Expected Output:  
    {expected_output}  
      
    Retrieval Context:  
    {retrieval_context}  
      
    JSON:  
    """  
      
    # Inject custom template to metric  
    metric = ContextualRecallMetric(evaluation_template=CustomTemplate)  
    metric.measure(...)  
    

[Edit this page](https://github.com/confident-ai/deepeval/edit/main/docs/docs/metrics-contextual-recall.mdx)

Last updated on **Apr 12, 2025** by **Jeffrey Ip**
