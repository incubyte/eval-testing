# Multimodal Contextual Precision

  * [](/)
  * Evaluation
  * Metrics
  * Multimodal Metrics
  * Multimodal Contextual Precision

On this page

# Multimodal Contextual Precision

The multimodal contextual precision metric measures your RAG pipeline's retriever by evaluating whether nodes in your `retrieval_context` that are relevant to the given `input` are ranked higher than irrelevant ones. `deepeval`'s multimodal contextual precision metric is a self-explaining MLLM-Eval, meaning it outputs a reason for its metric score.

info

The **Multimodal Contextual Precision** is the multimodal adaptation of DeepEval's [contextual precision metric](/docs/metrics-contextual-precision). It accepts images in addition to text for the `input`, `retrieval_context`, and `expected_output`.

## Required Arguments​

To use the `MultimodalContextualPrecisionMetric`, you'll have to provide the following arguments when creating a [`MLLMTestCase`](/docs/evaluation-test-cases#mllm-test-case):

  * `input`
  * `actual_output`
  * `expected_output`
  * `retrieval_context`

The `input` and `actual_output` are required to create an `MLLMTestCase` (and hence required by all metrics) even though they might not be used for metric calculation. Read the How Is It Calculated section below to learn more.

## Example​
    
    
    from deepeval import evaluate  
    from deepeval.metrics import MultimodalContextualPrecisionMetric  
    from deepeval.test_case import MLLMTestCase, MLLMImage  
      
    metric = MultimodalContextualPrecisionMetric()  
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
    

There are **SIX** optional parameters when creating a `MultimodalContextualPrecisionMetric`:

  * [Optional] `threshold`: a float representing the minimum passing threshold, defaulted to 0.5.
  * [Optional] `model`: a string specifying which of OpenAI's Multimodal GPT models to use, **OR** any custom MLLM model of type `DeepEvalBaseMLLM`. Defaulted to 'gpt-4o'.
  * [Optional] `include_reason`: a boolean which when set to `True`, will include a reason for its evaluation score. Defaulted to `True`.
  * [Optional] `strict_mode`: a boolean which when set to `True`, enforces a binary metric score: 1 for perfection, 0 otherwise. It also overrides the current threshold and sets it to 1. Defaulted to `False`.
  * [Optional] `async_mode`: a boolean which when set to `True`, enables [concurrent execution within the `measure()` method.](/docs/metrics-introduction#measuring-metrics-in-async) Defaulted to `True`.
  * [Optional] `verbose_mode`: a boolean which when set to `True`, prints the intermediate steps used to calculate said metric to the console, as outlined in the How Is It Calculated section. Defaulted to `False`.

## How Is It Calculated?​

The `MultimodalContextualPrecisionMetric` score is calculated according to the following equation:

Multimodal Contextual Precision=1Number of Relevant Nodes∑k=1n(Number of Relevant Nodes Up to Position kk×rk)\text{Multimodal Contextual Precision} = \frac{1}{\text{Number of Relevant Nodes}} \sum_{k=1}^{n} \left( \frac{\text{Number of Relevant Nodes Up to Position } k}{k} \times r_{k} \right)Multimodal Contextual Precision=Number of Relevant Nodes1​k=1∑n​(kNumber of Relevant Nodes Up to Position k​×rk​)

info

  * ** _k_** is the (i+1)th node in the `retrieval_context`
  * ** _n_** is the length of the `retrieval_context`
  * ** _r k_** is the binary relevance for the kth node in the `retrieval_context`. _r k_ = 1 for nodes that are relevant, 0 if not.

The `MultimodalContextualPrecisionMetric` first uses an MLLM to determine for each node in the `retrieval_context` whether it is relevant to the `input` based on information in the `expected_output`, before calculating the **weighted cumulative precision** as the contextual precision score. The weighted cumulative precision (WCP) is used because it:

  * **Emphasizes on Top Results** : WCP places a stronger emphasis on the relevance of top-ranked results. This emphasis is important because MLLMs tend to give more attention to earlier nodes in the `retrieval_context` (which may cause downstream hallucination if nodes are ranked incorrectly).
  * **Rewards Relevant Ordering** : WCP can handle varying degrees of relevance (e.g., "highly relevant", "somewhat relevant", "not relevant"). This is in contrast to metrics like precision, which treats all retrieved nodes as equally important.

A higher multimodal contextual precision score represents a greater ability of the retrieval system to correctly rank relevant nodes higher in the `retrieval_context`.

[Edit this page](https://github.com/confident-ai/deepeval/edit/main/docs/docs/multimodal-metrics-contextual-precision.mdx)

Last updated on **Apr 12, 2025** by **Jeffrey Ip**
