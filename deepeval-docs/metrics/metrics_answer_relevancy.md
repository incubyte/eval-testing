# Answer Relevancy

  * [](/)
  * Evaluation
  * Metrics
  * Answer Relevancy

On this page

# Answer Relevancy

The answer relevancy metric uses LLM-as-a-judge to measure the quality of your RAG pipeline's generator by evaluating how relevant the `actual_output` of your LLM application is compared to the provided `input`. `deepeval`'s answer relevancy metric is a self-explaining LLM-Eval, meaning it outputs a reason for its metric score.

tip

Here is a detailed guide on [RAG evaluation](/guides/guides-rag-evaluation), which we highly recommend as it explains everything about `deepeval`'s RAG metrics.

## Required Arguments​

To use the `AnswerRelevancyMetric`, you'll have to provide the following arguments when creating an [`LLMTestCase`](/docs/evaluation-test-cases#llm-test-case):

  * `input`
  * `actual_output`

The `input` and `actual_output` are required to create an `LLMTestCase` (and hence required by all metrics) even though they might not be used for metric calculation. Read the How Is It Calculated section below to learn more.

## Example​
    
    
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
    

There are **SEVEN** optional parameters when creating an `AnswerRelevancyMetric`:

  * [Optional] `threshold`: a float representing the minimum passing threshold, defaulted to 0.5.
  * [Optional] `model`: a string specifying which of OpenAI's GPT models to use, **OR** [any custom LLM model](/docs/metrics-introduction#using-a-custom-llm) of type `DeepEvalBaseLLM`. Defaulted to 'gpt-4o'.
  * [Optional] `include_reason`: a boolean which when set to `True`, will include a reason for its evaluation score. Defaulted to `True`.
  * [Optional] `strict_mode`: a boolean which when set to `True`, enforces a binary metric score: 1 for perfection, 0 otherwise. It also overrides the current threshold and sets it to 1. Defaulted to `False`.
  * [Optional] `async_mode`: a boolean which when set to `True`, enables [concurrent execution within the `measure()` method.](/docs/metrics-introduction#measuring-a-metric-in-async) Defaulted to `True`.
  * [Optional] `verbose_mode`: a boolean which when set to `True`, prints the intermediate steps used to calculate said metric to the console, as outlined in the How Is It Calculated section. Defaulted to `False`.
  * [Optional] `evaluation_template`: a class of type `AnswerRelevancyTemplate`, which allows you to override the default prompts used to compute the `AnswerRelevancyMetric` score. Defaulted to `deepeval`'s `AnswerRelevancyTemplate`.

### As a standalone​

You can also run the `AnswerRelevancyMetric` on a single test case as a standalone, one-off execution.
    
    
    ...  
      
    metric.measure(test_case)  
    print(metric.score, metric.reason)  
    

caution

This is great for debugging or if you wish to build your own evaluation pipeline, but you will **NOT** get the benefits (testing reports, Confident AI platform) and all the optimizations (speed, caching, computation) the `evaluate()` function or `deepeval test run` offers.

## How Is It Calculated?​

The `AnswerRelevancyMetric` score is calculated according to the following equation:

Answer Relevancy=Number of Relevant StatementsTotal Number of Statements\text{Answer Relevancy} = \frac{\text{Number of Relevant Statements}}{\text{Total Number of Statements}}Answer Relevancy=Total Number of StatementsNumber of Relevant Statements​

The `AnswerRelevancyMetric` first uses an LLM to extract all statements made in the `actual_output`, before using the same LLM to classify whether each statement is relevant to the `input`.

note

You can set the `verbose_mode` of **ANY** `deepeval` metric to `True` to debug the `measure()` method:
    
    
    ...  
      
    metric = AnswerRelevancyMetric(verbose_mode=True)  
    metric.measure(test_case)  
    

## Customize Your Template​

Since `deepeval`'s `AnswerRelevancyMetric` is evaluated by LLM-as-a-judge, you can likely improve your metric accuracy by [overriding `deepeval`'s default prompt templates](/docs/metrics-introduction#customizing-metric-prompts). This is especially helpful if:

  * You're using a [custom evaluation LLM](/guides/guides-using-custom-llms), especially for smaller models that have weaker instruction following capabilities.
  * You want to customize the examples used in the default `AnswerRelevancyTemplate` to better align with your expectations.

tip

You can learn what the default `AnswerRelevancyTemplate` looks like [here on GitHub](https://github.com/confident-ai/deepeval/blob/main/deepeval/metrics/answer_relevancy/template.py), and should read the How Is It Calculated section above to understand how you can tailor it to your needs.

Here's a quick example of how you can override the statement generation step of the `AnswerRelevancyMetric` algorithm:
    
    
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
      
    JSON:  
    """  
      
    # Inject custom template to metric  
    metric = AnswerRelevancyMetric(evaluation_template=CustomTemplate)  
    metric.measure(...)  
    

[Edit this page](https://github.com/confident-ai/deepeval/edit/main/docs/docs/metrics-answer-relevancy.mdx)

Last updated on **Apr 12, 2025** by **Jeffrey Ip**
