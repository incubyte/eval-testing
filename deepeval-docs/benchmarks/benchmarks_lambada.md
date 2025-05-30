# LAMBADA

  * [](/)
  * Evaluation
  * Benchmarks
  * LAMBADA

On this page

# LAMBADA

**LAMBADA** (_LAnguage Modeling Broadened to Account for Discourse Aspects_) evaluates an LLM's ability to comprehend context and understand discourse. This dataset includes 10,000 passages sourced from BooksCorpus, each requiring the LLM to predict the final word of a sentence. To explore the dataset in more detail, check out the [original LAMBADA paper](https://arxiv.org/abs/1606.06031).

tip

The `LAMBADA` dataset is specifically designed so that humans cannot predict the final word of the last sentence without the preceding context, making it an effective benchmark for evaluating a model's **broad comprehension**.

## Arguments​

There are **TWO** optional arguments when using the `LAMBADA` benchmark:

  * [Optional] `n_problems`: the number of problems for model evaluation. By default, this is set to 5153 (all problems).
  * [Optional] `n_shots`: the number of examples for few-shot learning. This is **set to 5** by default and **cannot exceed 5**.

## Example​

The code below assesses a custom `mistral_7b` model ([click here to learn how to use **ANY** custom LLM](/docs/benchmarks-introduction#benchmarking-your-llm)) on 10 problems in `LAMBADA` using 3-shot CoT prompting.
    
    
    from deepeval.benchmarks import LAMBADA  
      
    # Define benchmark with n_problems and shots  
    benchmark = LAMBADA(  
        n_problems=10,  
        n_shots=3,  
    )  
      
    # Replace 'mistral_7b' with your own custom model  
    benchmark.evaluate(model=mistral_7b)  
    print(benchmark.overall_score)  
    

The `overall_score` for this benchmark ranges from 0 to 1, where 1 signifies perfect performance and 0 indicates no correct answers. The model's score, based on **exact matching** , is calculated by determining the proportion of questions for which the model predicts the **precise correct target word** in relation to the total number of questions.

tip

As a result, utilizing more few-shot prompts (`n_shots`) can greatly improve the model's robustness in generating answers in the exact correct format and boost the overall score.

[Edit this page](https://github.com/confident-ai/deepeval/edit/main/docs/docs/benchmarks-lambada.mdx)

Last updated on **Apr 12, 2025** by **Jeffrey Ip**
