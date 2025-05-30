# GSM8K

  * [](/)
  * Evaluation
  * Benchmarks
  * GSM8K

On this page

# GSM8K

The **GSM8K** benchmark comprises 1,319 grade school math word problems, each crafted by expert human problem writers. These problems involve elementary arithmetic operations (+ − ×÷) and require between 2 to 8 steps to solve. The dataset is designed to evaluate an LLM’s ability to perform multi-step mathematical reasoning. For more information, you can [read the original GSM8K paper here](https://arxiv.org/abs/2110.14168).

## Arguments​

There are **THREE** optional arguments when using the `GSM8K` benchmark:

  * [Optional] `n_problems`: the number of problems for model evaluation. By default, this is set to 1319 (all problems in the benchmark).
  * [Optional] `n_shots`: the number of "shots" to use for few-shot learning. This number ranges strictly from 0-3, and is **set to 3 by default**.
  * [Optional] `enable_cot`: a boolean that determines if CoT prompting is used for evaluation. This is set to `True` by default.

info

**Chain-of-Thought (CoT) prompting** is an approach where the model is prompted to articulate its reasoning process to arrive at an answer. You can learn more about CoT [here](https://arxiv.org/abs/2201.11903).

## Example​

The code below assesses a custom `mistral_7b` model ([click here to learn how to use **ANY** custom LLM](/docs/benchmarks-introduction#benchmarking-your-llm)) on 10 problems in `GSM8K` using 3-shot CoT prompting.
    
    
    from deepeval.benchmarks import GSM8K  
      
    # Define benchmark with n_problems and shots  
    benchmark = GSM8K(  
        n_problems=10,  
        n_shots=3,  
        enable_cot=True  
    )  
      
    # Replace 'mistral_7b' with your own custom model  
    benchmark.evaluate(model=mistral_7b)  
    print(benchmark.overall_score)  
    

The `overall_score` for this benchmark ranges from 0 to 1, where 1 signifies perfect performance and 0 indicates no correct answers. The model's score, based on **exact matching** , is calculated by determining the proportion of math word problems for which the model produces the precise correct answer number (e.g. '56') in relation to the total number of questions.

As a result, utilizing more few-shot prompts (`n_shots`) can greatly improve the model's robustness in generating answers in the exact correct format and boost the overall score.

[Edit this page](https://github.com/confident-ai/deepeval/edit/main/docs/docs/benchmarks-gsm8k.mdx)

Last updated on **Apr 12, 2025** by **Jeffrey Ip**
