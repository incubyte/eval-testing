# RAGAS

  * [](/)
  * Evaluation
  * Metrics
  * RAGAS

On this page

# RAGAS

The RAGAS metric is the average of four distinct metrics:

  * `RAGASAnswerRelevancyMetric`
  * `RAGASFaithfulnessMetric`
  * `RAGASContextualPrecisionMetric`
  * `RAGASContextualRecallMetric`

It provides a score to holistically evaluate of your RAG pipeline's generator and retriever.

WHAT'S THE DIFFERENCE?

The `RAGASMetric` uses the `ragas` library under the hood and are available on `deepeval` with the intention to allow users of `deepeval` can have access to `ragas` in `deepeval`'s ecosystem as well. They are implemented in an almost identical way to `deepeval`'s default RAG metrics. However there are a few differences, including but not limited to:

  * `deepeval`'s RAG metrics generates a reason that corresponds to the score equation. Although both `ragas` and `deepeval` has equations attached to their default metrics, `deepeval` incorperates an LLM judges' reasoning along the way.
  * `deepeval`'s RAG metrics are debuggable - meaning you can inspect the LLM judges' judgements along the way to see why the score is a certain way.
  * `deepeval`'s RAG metrics are JSON confineable. You'll often meet `NaN` scores in `ragas` because of invalid JSONs generated - but `deepeval` offers a way for you to use literally any custom LLM for evaluation and [JSON confine them in a few lines of code.](/guides/guides-using-custom-llms)
  * `deepeval`'s RAG metrics integrates **fully** with `deepeval`'s ecosystem. This means you'll get access to metrics caching, native support for `pytest` integrations, first-class error handling, available on Confident AI, and so much more.

Due to these reasons, we highly recommend that you use `deepeval`'s RAG metrics instead. They're proven to work, and if not better according to [examples shown in some studies.](https://arxiv.org/pdf/2409.06595)

## Required Arguments​

To use the `RagasMetric`, you'll have to provide the following arguments when creating an [`LLMTestCase`](/docs/evaluation-test-cases#llm-test-case):

  * `input`
  * `actual_output`
  * `expected_output`
  * `retrieval_context`

## Example​

First, install `ragas`:
    
    
    pip install ragas  
    

Then, use it within `deepeval`:
    
    
    from deepeval import evaluate  
    from deepeval.metrics.ragas import RagasMetric  
    from deepeval.test_case import LLMTestCase  
      
    # Replace this with the actual output from your LLM application  
    actual_output = "We offer a 30-day full refund at no extra cost."  
      
    # Replace this with the expected output from your RAG generator  
    expected_output = "You are eligible for a 30 day full refund at no extra cost."  
      
    # Replace this with the actual retrieved context from your RAG pipeline  
    retrieval_context = ["All customers are eligible for a 30 day full refund at no extra cost."]  
      
    metric = RagasMetric(threshold=0.5, model="gpt-3.5-turbo")  
    test_case = LLMTestCase(  
        input="What if these shoes don't fit?",  
        actual_output=actual_output,  
        expected_output=expected_output,  
        retrieval_context=retrieval_context  
    )  
      
    metric.measure(test_case)  
    print(metric.score)  
      
    # or evaluate test cases in bulk  
    evaluate([test_case], [metric])  
    

There are **THREE** optional parameters when creating a `RagasMetric`:

  * [Optional] `threshold`: a float representing the minimum passing threshold, defaulted to 0.5.
  * [Optional] `model`: a string specifying which of OpenAI's GPT models to use, **OR** any one of langchain's [chat models](https://python.langchain.com/docs/integrations/chat/) of type `BaseChatModel`. Defaulted to 'gpt-3.5-turbo'.
  * [Optional] `embeddings`: any one of langchain's [embedding models](https://python.langchain.com/docs/integrations/text_embedding) of type `Embeddings`. Custom `embeddings` provided to the `RagasMetric` will only be used in the `RAGASAnswerRelevancyMetric`, since it is the only metric that requires embeddings for calculating cosine similarity.

info

You can also choose to import and execute each metric individually:
    
    
    from deepeval.metrics.ragas import RAGASAnswerRelevancyMetric  
    from deepeval.metrics.ragas import RAGASFaithfulnessMetric  
    from deepeval.metrics.ragas import RAGASContextualRecallMetric  
    from deepeval.metrics.ragas import RAGASContextualPrecisionMetric  
    

These metrics accept the same arguments as the `RagasMetric`.

[Edit this page](https://github.com/confident-ai/deepeval/edit/main/docs/docs/metrics-ragas.mdx)

Last updated on **Apr 12, 2025** by **Jeffrey Ip**
