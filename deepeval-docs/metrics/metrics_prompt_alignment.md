# Prompt Alignment

  * [](/)
  * Evaluation
  * Metrics
  * Prompt Alignment

On this page

# Prompt Alignment

The prompt alignment metric uses LLM-as-a-judge to measure whether your LLM application is able to generate `actual_output`s that aligns with any **instructions** specified in your prompt template. `deepeval`'s prompt alignment metric is a self-explaining LLM-Eval, meaning it outputs a reason for its metric score.

tip

Not sure if this metric is for you? Run the follow command to find out:
    
    
    deepeval recommend metrics  
    

## Required Arguments​

To use the `PromptAlignmentMetric`, you'll have to provide the following arguments when creating an [`LLMTestCase`](/docs/evaluation-test-cases#llm-test-case):

  * `input`
  * `actual_output`

The `input` and `actual_output` are required to create an `LLMTestCase` (and hence required by all metrics) even though they might not be used for metric calculation. Read the How Is It Calculated section below to learn more.

## Example​
    
    
    from deepeval import evaluate  
    from deepeval.test_case import LLMTestCase  
    from deepeval.metrics import PromptAlignmentMetric  
      
    metric = PromptAlignmentMetric(  
        prompt_instructions=["Reply in all uppercase"],  
        model="gpt-4",  
        include_reason=True  
    )  
    test_case = LLMTestCase(  
        input="What if these shoes don't fit?",  
        # Replace this with the actual output from your LLM application  
        actual_output="We offer a 30-day full refund at no extra cost."  
    )  
      
    # To run metric as a standalone  
    # metric.measure(test_case)  
    # print(metric.score, metric.reason)  
      
    evaluate(test_cases=[test_case], metrics=[metric])  
    

There are **ONE** mandatory and **SIX** optional parameters when creating an `PromptAlignmentMetric`:

  * `prompt_instructions`: a list of strings specifying the instructions you want followed in your prompt template.
  * [Optional] `threshold`: a float representing the minimum passing threshold, defaulted to 0.5.
  * [Optional] `model`: a string specifying which of OpenAI's GPT models to use, **OR** [any custom LLM model](/docs/metrics-introduction#using-a-custom-llm) of type `DeepEvalBaseLLM`. Defaulted to 'gpt-4o'.
  * [Optional] `include_reason`: a boolean which when set to `True`, will include a reason for its evaluation score. Defaulted to `True`.
  * [Optional] `strict_mode`: a boolean which when set to `True`, enforces a binary metric score: 1 for perfection, 0 otherwise. It also overrides the current threshold and sets it to 1. Defaulted to `False`.
  * [Optional] `async_mode`: a boolean which when set to `True`, enables [concurrent execution within the `measure()` method.](/docs/metrics-introduction#measuring-a-metric-in-async) Defaulted to `True`.
  * [Optional] `verbose_mode`: a boolean which when set to `True`, prints the intermediate steps used to calculate said metric to the console, as outlined in the How Is It Calculated section. Defaulted to `False`.

### As a standalone​

You can also run the `PromptAlignmentMetric` on a single test case as a standalone, one-off execution.
    
    
    ...  
      
    metric.measure(test_case)  
    print(metric.score, metric.reason)  
    

caution

This is great for debugging or if you wish to build your own evaluation pipeline, but you will **NOT** get the benefits (testing reports, Confident AI platform) and all the optimizations (speed, caching, computation) the `evaluate()` function or `deepeval test run` offers.

## How Is It Calculated?​

The `PromptAlignmentMetric` score is calculated according to the following equation:

Prompt Alignment=Number of Instructions FollowedTotal Number of Instructions\text{Prompt Alignment} = \frac{\text{Number of Instructions Followed}}{\text{Total Number of Instructions}}Prompt Alignment=Total Number of InstructionsNumber of Instructions Followed​

The `PromptAlignmentMetric` uses an LLM to classify whether each prompt instruction is followed in the `actual_output` using additional context from the `input`.

tip

By providing an initial list of `prompt_instructions` instead of the entire prompt template, the `PromptAlignmentMetric` is able to more accurately determine whether the core instructions laid out in your prompt template is followed.

[Edit this page](https://github.com/confident-ai/deepeval/edit/main/docs/docs/metrics-prompt-alignment.mdx)

Last updated on **Apr 12, 2025** by **Jeffrey Ip**
