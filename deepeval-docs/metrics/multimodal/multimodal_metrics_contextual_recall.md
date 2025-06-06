# Multimodal Contextual Recall

  * [](/)
  * Evaluation
  * Metrics
  * Multimodal Metrics
  * Multimodal Contextual Recall

On this page

# Multimodal Contextual Recall

The multimodal contextual recall metric measures the quality of your RAG pipeline's retriever by evaluating the extent of which the `retrieval_context` aligns with the `expected_output`. `deepeval`'s contextual recall metric is a self-explaining MLLM-Eval, meaning it outputs a reason for its metric score.

info

The **Multimodal Contextual Recall** is the multimodal adaptation of DeepEval's [contextual recall metric](/docs/metrics-contextual-recall). It accepts images in addition to text for the `input`, `actual_output`, `expected_output`, and `retrieval_context`.

## Required Arguments​

To use the `MultimodalContextualRecallMetric`, you'll have to provide the following arguments when creating a [`MLLMTestCase`](/docs/evaluation-test-cases#mllm-test-case):

  * `input`
  * `actual_output`
  * `expected_output`
  * `retrieval_context`

The `input` and `actual_output` are required to create an `MLLMTestCase` (and hence required by all metrics) even though they might not be used for metric calculation. Read the How Is It Calculated section below to learn more.

## Example​
    
    
    from deepeval import evaluate  
    from deepeval.metrics import MultimodalContextualRecallMetric  
    from deepeval.test_case import MLLMTestCase, MLLMImage  
      
    metric = MultimodalContextualRecallMetric()  
    test_case = MLLMTestCase(  
        input=["Tell me about some landmarks in France"],  
        actual_output=[  
            "France is home to iconic landmarks like the Eiffel Tower in Paris.",  
            MLLMImage(...)  
        ],  
        expected_output=[  
            "The Eiffel Tower is located in Paris, France.",  
            MLLMImage(...)  
        ],  
        retrieval_context=[  
            MLLMImage(...),  
            "The Eiffel Tower is a wrought-iron lattice tower built in the late 19th century.",  
            MLLMImage(...)  
        ],  
    )  
      
      
    metric.measure(test_case)  
    print(metric.score)  
    print(metric.reason)  
      
    # or evaluate test cases in bulk  
    evaluate([test_case], [metric])  
    

There are **SIX** optional parameters when creating a `MultimodalContextualRecallMetric`:

  * [Optional] `threshold`: a float representing the minimum passing threshold, defaulted to 0.5.
  * [Optional] `model`: a string specifying which of OpenAI's Multimodal GPT models to use, **OR** any custom MLLM model of type `DeepEvalBaseMLLM`. Defaulted to 'gpt-4o'.
  * [Optional] `include_reason`: a boolean which when set to `True`, will include a reason for its evaluation score. Defaulted to `True`.
  * [Optional] `strict_mode`: a boolean which when set to `True`, enforces a binary metric score: 1 for perfection, 0 otherwise. It also overrides the current threshold and sets it to 1. Defaulted to `False`.
  * [Optional] `async_mode`: a boolean which when set to `True`, enables [concurrent execution within the `measure()` method.](/docs/metrics-introduction#measuring-metrics-in-async) Defaulted to `True`.
  * [Optional] `verbose_mode`: a boolean which when set to `True`, prints the intermediate steps used to calculate said metric to the console, as outlined in the How Is It Calculated section. Defaulted to `False`.

## How Is It Calculated?​

The `MultimodalContextualRecallMetric` score is calculated according to the following equation:

Multimodal Contextual Recall=Number of Attributable StatementsTotal Number of Statements\text{Multimodal Contextual Recall} = \frac{\text{Number of Attributable Statements}}{\text{Total Number of Statements}}Multimodal Contextual Recall=Total Number of StatementsNumber of Attributable Statements​

The `MultimodalContextualRecallMetric` first uses an MLLM to extract all **statements and images in the`expected_output`**, before using the same MLLM to classify whether each statement and image can be attributed to nodes in the `retrieval_context`.

info

We use the `expected_output` instead of the `actual_output` because we're measuring the quality of the RAG retriever for a given ideal output.

A higher contextual recall score represents a greater ability of the retrieval system to capture all relevant information from the total available relevant set within your knowledge base.

[Edit this page](https://github.com/confident-ai/deepeval/edit/main/docs/docs/multimodal-metrics-contextual-recall.mdx)

Last updated on **Apr 12, 2025** by **Jeffrey Ip**
