# Contextual Relevancy

  * [](/)
  * Evaluation
  * Metrics
  * Contextual Relevancy

On this page

# Contextual Relevancy

The contextual relevancy metric uses LLM-as-a-judge to measure the quality of your RAG pipeline's retriever by evaluating the overall relevance of the information presented in your `retrieval_context` for a given `input`. `deepeval`'s contextual relevancy metric is a self-explaining LLM-Eval, meaning it outputs a reason for its metric score.

tip

Not sure if the `ContextualRelevancyMetric` is suitable for your use case? Run the follow command to find out:
    
    
    deepeval recommend metrics  
    

## Required Arguments​

To use the `ContextualRelevancyMetric`, you'll have to provide the following arguments when creating an [`LLMTestCase`](/docs/evaluation-test-cases#llm-test-case):

  * `input`
  * `actual_output`
  * `retrieval_context`

note

Similar to `ContextualPrecisionMetric`, the `ContextualRelevancyMetric` uses `retrieval_context` from your RAG pipeline for evaluation.

The `input` and `actual_output` are required to create an `LLMTestCase` (and hence required by all metrics) even though they might not be used for metric calculation. Read the How Is It Calculated section below to learn more.

## Example​
    
    
    from deepeval import evaluate  
    from deepeval.test_case import LLMTestCase  
    from deepeval.metrics import ContextualRelevancyMetric  
      
    # Replace this with the actual output from your LLM application  
    actual_output = "We offer a 30-day full refund at no extra cost."  
      
    # Replace this with the actual retrieved context from your RAG pipeline  
    retrieval_context = ["All customers are eligible for a 30 day full refund at no extra cost."]  
      
    metric = ContextualRelevancyMetric(  
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
    

There are **SEVEN** optional parameters when creating a `ContextualRelevancyMetricMetric`:

  * [Optional] `threshold`: a float representing the minimum passing threshold, defaulted to 0.5.
  * [Optional] `model`: a string specifying which of OpenAI's GPT models to use, **OR** [any custom LLM model](/docs/metrics-introduction#using-a-custom-llm) of type `DeepEvalBaseLLM`. Defaulted to 'gpt-4o'.
  * [Optional] `include_reason`: a boolean which when set to `True`, will include a reason for its evaluation score. Defaulted to `True`.
  * [Optional] `strict_mode`: a boolean which when set to `True`, enforces a binary metric score: 1 for perfection, 0 otherwise. It also overrides the current threshold and sets it to 1. Defaulted to `False`.
  * [Optional] `async_mode`: a boolean which when set to `True`, enables [concurrent execution within the `measure()` method.](/docs/metrics-introduction#measuring-metrics-in-async) Defaulted to `True`.
  * [Optional] `verbose_mode`: a boolean which when set to `True`, prints the intermediate steps used to calculate said metric to the console, as outlined in the How Is It Calculated section. Defaulted to `False`.
  * [Optional] `evaluation_template`: a class of type `ContextualRelevancyTemplate`, which allows you to override the default prompt templates used to compute the `ContextualRelevancyMetric` score. You can learn what the default prompts looks like [here](https://github.com/confident-ai/deepeval/blob/main/deepeval/metrics/contextual_relevancy/template.py), and should read the How Is It Calculated section below to understand how you can tailor it to your needs. Defaulted to `deepeval`'s `ContextualRelevancyTemplate`.

### As a standalone​

You can also run the `ContextualRelevancyMetric` on a single test case as a standalone, one-off execution.
    
    
    ...  
      
    metric.measure(test_case)  
    print(metric.score, metric.reason)  
    

caution

This is great for debugging or if you wish to build your own evaluation pipeline, but you will **NOT** get the benefits (testing reports, Confident AI platform) and all the optimizations (speed, caching, computation) the `evaluate()` function or `deepeval test run` offers.

## How Is It Calculated?​

The `ContextualRelevancyMetric` score is calculated according to the following equation:

Contextual Relevancy=Number of Relevant StatementsTotal Number of Statements\text{Contextual Relevancy} = \frac{\text{Number of Relevant Statements}}{\text{Total Number of Statements}}Contextual Relevancy=Total Number of StatementsNumber of Relevant Statements​

Although similar to how the `AnswerRelevancyMetric` is calculated, the `ContextualRelevancyMetric` first uses an LLM to extract all statements made in the `retrieval_context` instead, before using the same LLM to classify whether each statement is relevant to the `input`.

## Customize Your Template​

Since `deepeval`'s `ContextualRelevancyMetric` is evaluated by LLM-as-a-judge, you can likely improve your metric accuracy by [overriding `deepeval`'s default prompt templates](/docs/metrics-introduction#customizing-metric-prompts). This is especially helpful if:

  * You're using a [custom evaluation LLM](/guides/guides-using-custom-llms), especially for smaller models that have weaker instruction following capabilities.
  * You want to customize the examples used in the default `ContextualRelevancyTemplate` to better align with your expectations.

tip

You can learn what the default `ContextualRelevancyTemplate` looks like [here on GitHub](https://github.com/confident-ai/deepeval/blob/main/deepeval/metrics/contextual_relevancy/template.py), and should read the How Is It Calculated section above to understand how you can tailor it to your needs.

Here's a quick example of how you can override the relevancy classification step of the `ContextualRelevancyMetric` algorithm:
    
    
    from deepeval.metrics import ContextualRelevancyMetric  
    from deepeval.metrics.contextual_relevancy import ContextualRelevancyTemplate  
      
    # Define custom template  
    class CustomTemplate(ContextualRelevancyTemplate):  
        @staticmethod  
        def generate_verdicts(input: str, context: str):  
            return f"""Based on the input and context, please generate a JSON object to indicate whether each statement found in the context is relevant to the provided input.  
      
    Example JSON:  
    {{  
        "verdicts": [  
            {{  
                "verdict": "yes",  
                "statement": "...",  
            }}  
        ]  
    }}  
    **  
      
    Input:  
    {input}  
      
    Context:  
    {context}  
      
    JSON:  
    """  
      
    # Inject custom template to metric  
    metric = ContextualRelevancyMetric(evaluation_template=CustomTemplate)  
    metric.measure(...)  
    

[Edit this page](https://github.com/confident-ai/deepeval/edit/main/docs/docs/metrics-contextual-relevancy.mdx)

Last updated on **Apr 12, 2025** by **Jeffrey Ip**
