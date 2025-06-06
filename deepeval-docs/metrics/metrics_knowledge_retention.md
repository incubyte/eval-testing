# Knowledge Retention

  * [](/)
  * Evaluation
  * Metrics
  * Conversational Metrics
  * Knowledge Retention

On this page

# Knowledge Retention

The knowledge retention metric is a conversational metric that determines whether your LLM chatbot is able to retain factual information presented **throughout a conversation**.

## Required Arguments​

To use the `KnowledgeRetentionMetric`, you'll have to provide the following arguments when creating a [`ConversationalTestCase`](/docs/evaluation-test-cases#conversational-test-case):

  * `turns`

Additionally, each `LLMTestCase`s in `turns` requires the following arguments:

  * `input`
  * `actual_output`

## Example​

Let's take this conversation as an example:
    
    
    from deepeval.test_case import LLMTestCase  
      
    turns = [  
        LLMTestCase(  
            input="",  
            actual_output="Hello! I'm here to assist you with opening a new bank account. To start, may I have your full name, please?"  
        ),  
        LLMTestCase(  
            input="Sure, it's Alex Johnson. I also have a dog called Jacky.",  
            actual_output="Great, Alex! Now, could you please provide your current address?"  
        ),  
        LLMTestCase(  
            input="123 Maple Street, Springfield.",  
            actual_output="Is that all?"  
        ),  
        LLMTestCase(  
            input="I also have another address at 123 Broadway, NYC.",  
            actual_output="Wonderful. Next, I'll need your bank account number where we can link this new account."  
        ),  
        LLMTestCase(  
            input="456789123",  
            actual_output="This account number seems invalid, can you please double-check?"  
        ),  
        LLMTestCase(  
            input="Sorry you're right, its 456789124.",  
            actual_output="Thank you. And for our next step, could you tell me your date of birth?"  
        ),  
        LLMTestCase(  
            input="It's July 9th.",  
            actual_output="What about the year?"  
        ),  
        LLMTestCase(  
            input="1990",  
            actual_output="Got it. Now, for security purposes, could you share your mother's maiden name?"  
        ),  
        LLMTestCase(  
            input="It's Smith.",  
            actual_output="Excellent. Just a few more details. What is your phone number?"  
        ),  
        LLMTestCase(  
            input="555-0102",  
            actual_output="Great, we're almost done. Could you remind me of your full name for the account documentation?"  
        ),  
        LLMTestCase(  
            input="Didn't I tell you already? It's Alex Johnson.",  
            actual_output="What is your bank account number?"  
        ),  
        LLMTestCase(  
            input="Yes, I did... It's 456789124. Are you not keeping track of this?",  
            actual_output="One last question, what is the country code of your phone number?"  
        ),  
        LLMTestCase(  
            input="+44",  
            actual_output="Thank you, Alex, for bearing with me. We now have all the information we need to proceed with opening your new bank account. I appreciate your cooperation and patience throughout this process."  
        )  
    ]  
    

You can use the `KnowledgeRetentionMetric` as follows:
    
    
    from deepeval import evaluate  
    from deepeval.test_case import ConversationalTestCase  
    from deepeval.metrics import KnowledgeRetentionMetric  
    ...  
      
    convo_test_case = ConversationalTestCase(turns=turns)  
    metric = KnowledgeRetentionMetric(threshold=0.5)  
      
    # To run metric as a standalone  
    # metric.measure(convo_test_case)  
    # print(metric.score, metric.reason)  
      
    evaluate(test_cases=[convo_test_case], metrics=[metric])  
    

There are **FIVE** optional parameters when creating a `KnowledgeRetentionMetric`:

  * [Optional] `threshold`: a float representing the maximum passing threshold, defaulted to 0.5.
  * [Optional] `model`: a string specifying which of OpenAI's GPT models to use, **OR** [any custom LLM model](/docs/metrics-introduction#using-a-custom-llm) of type `DeepEvalBaseLLM`. Defaulted to 'gpt-4o'.
  * [Optional] `include_reason`: a boolean which when set to `True`, will include a reason for its evaluation score. Defaulted to `True`.
  * [Optional] `strict_mode`: a boolean which when set to `True`, enforces a binary metric score: 1 for perfection, 0 otherwise. It also overrides the current threshold and sets it to 0. Defaulted to `False`.
  * [Optional] `verbose_mode`: a boolean which when set to `True`, prints the intermediate steps used to calculate said metric to the console, as outlined in the How Is It Calculated section. Defaulted to `False`.

### As a standalone​

You can also run the `KnowledgeRetentionMetric` on a single test case as a standalone, one-off execution.
    
    
    ...  
      
    metric.measure(test_case)  
    print(metric.score, metric.reason)  
    

caution

This is great for debugging or if you wish to build your own evaluation pipeline, but you will **NOT** get the benefits (testing reports, Confident AI platform) and all the optimizations (speed, caching, computation) the `evaluate()` function or `deepeval test run` offers.

## How Is It Calculated?​

The `KnowledgeRetentionMetric` score is calculated according to the following equation:

Knowledge Retention=Number of Turns without Knowledge AttritionsTotal Number of Turns\text{Knowledge Retention} = \frac{\text{Number of Turns without Knowledge Attritions}}{\text{Total Number of Turns}}Knowledge Retention=Total Number of TurnsNumber of Turns without Knowledge Attritions​

The `KnowledgeRetentionMetric` first uses an LLM to extract knowledge gained throughout `turns`, before using the same LLM to determine whether each corresponding LLM responses indicates an inability to recall said knowledge.

info

Unlike other metrics, the `KnowledgeRetentionMetric` is still in beta, and we would love to hear any suggestions on our [discord channel.](https://discord.com/invite/a3K9c8GRGt)

[Edit this page](https://github.com/confident-ai/deepeval/edit/main/docs/docs/metrics-knowledge-retention.mdx)

Last updated on **Apr 12, 2025** by **Jeffrey Ip**
