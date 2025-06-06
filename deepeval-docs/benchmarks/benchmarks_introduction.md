# Introduction

  * [](/)
  * Evaluation
  * Benchmarks
  * Introduction

On this page

# Introduction

## Quick Summary​

LLM benchmarking provides a standardized way to quantify LLM performances across a range of different tasks. `deepeval` offers several state-of-the-art, research-backed benchmarks for you to quickly evaluate **ANY** custom LLM of your choice. These benchmarks include:

  * BIG-Bench Hard
  * HellaSwag
  * MMLU (Massive Multitask Language Understanding)
  * DROP
  * TruthfulQA
  * HumanEval
  * GSM8K

To benchmark your LLM, you will need to wrap your LLM implementation (which could be anything such as a simple API call to OpenAI, or a Hugging Face transformers model) within `deepeval`'s `DeepEvalBaseLLM` class. Visit the [custom models section](/docs/metrics-introduction#using-a-custom-llm) for a detailed guide on how to create a custom model object.

info

In `deepeval`, anyone can benchmark **ANY** LLM of their choice in just a few lines of code. All benchmarks offered by `deepeval` follows the implementation of their original research papers.

## What are LLM Benchmarks?​

LLM benchmarks are a set of standardized tests designed to evaluate the performance of an LLM on various skills, such as reasoning and comprehension. A benchmark is made up of:

  * one or more **tasks** , where each task is its own evaluation dataset with target labels (or `expected_outputs`)
  * a **scorer** , to determine whether predictions from your LLM is correct or not (by using target labels as reference)
  * various **prompting techniques** , which can be either involve few-shot learning and/or CoTs prompting

The LLM to be evaluated will generate "predictions" for each tasks in a benchmark aided by the outlined prompting techniques, while the scorer will score these predictions by using the target labels as reference. There is no standard way of scoring across different benchmarks, but most simply uses the **exact match scorer** for evaluation.

tip

A target label in a benchmark dataset is simply the `expected_output` in `deepeval` terms.

## Benchmarking Your LLM​

Below is an example of how to evaluate a [Mistral 7B model](https://huggingface.co/docs/transformers/model_doc/mistral) (exposed through Hugging Face's `transformers` library) against the `MMLU` benchmark.

danger

Often times, LLMs you're trying to benchmark can fail to generate correctly structured outputs for these public benchmarks to work. These public benchmarks, as you'll learn later, mostly require outputs in the form of single letters as they are often presented in MCQ format, and the failure to generate nothing else but single letters can cause these benchmarks to give faulty results. If you ever run into issues where benchmark scores are absurdly low, it is likely your LLM is not generating valid outputs.

There are a few ways to go around this, such as fine-tuning the model on specific tasks or datasets that closely resemble the target task (e.g., MCQs). However, this is complicated and fortunately in `deepeval` there is no need for this.

**Simply follow[this quick guide](/guides/guides-using-custom-llms#json-confinement-for-custom-llms) to learn how to generate the correct outputs in your custom LLM implementation to benchmark your custom LLM.**

### Create A Custom LLM​

Start by creating a custom model which **you will be benchmarking** by inheriting the `DeepEvalBaseLLM` class (visit the [custom models section](/docs/metrics-introduction#using-a-custom-llm) for a full guide on how to create a custom model):
    
    
    from transformers import AutoModelForCausalLM, AutoTokenizer  
    from deepeval.models.base_model import DeepEvalBaseLLM  
      
    class Mistral7B(DeepEvalBaseLLM):  
        def __init__(  
            self,  
            model,  
            tokenizer  
        ):  
            self.model = model  
            self.tokenizer = tokenizer  
      
        def load_model(self):  
            return self.model  
      
        def generate(self, prompt: str) -> str:  
            model = self.load_model()  
      
            device = "cuda" # the device to load the model onto  
      
            model_inputs = self.tokenizer([prompt], return_tensors="pt").to(device)  
            model.to(device)  
      
            generated_ids = model.generate(**model_inputs, max_new_tokens=100, do_sample=True)  
            return self.tokenizer.batch_decode(generated_ids)[0]  
      
        async def a_generate(self, prompt: str) -> str:  
            return self.generate(prompt)  
      
        # This is optional.  
        def batch_generate(self, promtps: List[str]) -> List[str]:  
            model = self.load_model()  
            device = "cuda" # the device to load the model onto  
      
            model_inputs = self.tokenizer(promtps, return_tensors="pt").to(device)  
            model.to(device)  
      
            generated_ids = model.generate(**model_inputs, max_new_tokens=100, do_sample=True)  
            return self.tokenizer.batch_decode(generated_ids)  
      
        def get_model_name(self):  
            return "Mistral 7B"  
      
    model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-v0.1")  
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")  
      
    mistral_7b = Mistral7B(model=model, tokenizer=tokenizer)  
    print(mistral_7b("Write me a joke"))  
    

tip

Notice you can also **optionally** define a `batch_generate()` method if your LLM offers an API to generate outputs in batches.

Next, define a MMLU benchmark using the `MMLU` class:
    
    
    from deepeval.benchmarks import MMLU  
    ...  
      
    benchmark = MMLU()  
    

Lastly, call the `evaluate()` method to benchmark your custom LLM:
    
    
    ...  
      
    # When you set batch_size, outputs for benchmarks will be generated in batches  
    # if `batch_generate()` is implemented for your custom LLM  
    results = benchmark.evaluate(model=mistral_7b, batch_size=5)  
    print("Overall Score: ", results)  
    

✅ **Congraulations! You can now evaluate any custom LLM of your choice on all LLM benchmarks offered by`deepeval`.**

tip

When you set `batch_size`, outputs for benchmarks will be generated in batches if `batch_generate()` is implemented for your custom LLM. This can speed up benchmarking by a lot.

The `batch_size` parameter is available for all benchmarks **except** for `HumanEval` and `GSM8K`.

After running an evaluation, you can access the results in multiple ways to analyze the performance of your model. This includes the overall score, task-specific scores, and details about each prediction.

### Overall Score​

The `overall_score`, which represents your model's performance across all specified tasks, can be accessed through the `overall_score` attribute:
    
    
    ...  
      
    print("Overall Score:", benchmark.overall_score)  
    

### Task Scores​

Individual task scores can be accessed through the `task_scores` attribute:
    
    
    ...  
      
    print("Task-specific Scores: ", benchmark.task_scores)  
    

The `task_scores` attribute outputs a pandas DataFrame containing information about scores achieved in various tasks. Below is an example DataFrame:

Task| Score  
---|---  
high_school_computer_science| 0.75  
astronomy| 0.93  
  
### Prediction Details​

You can also access a comprehensive breakdown of your model's predictions across different tasks through the `predictions` attribute:
    
    
    ...  
      
    print("Detailed Predictions: ", benchmark.predictions)  
    

The benchmark.predictions attribute also yields a pandas DataFrame containing detailed information about predictions made by the model. Below is an example DataFrame:

Task| Input| Prediction| Correct  
---|---|---|---  
high_school_computer_science| In Python 3, which of the following function convert a string to an int in python?| A| 0  
high_school_computer_science| Let x = 1. What is x << 3 in Python 3?| B| 1  
...| ...| ...| ...  
  
## Configurating LLM Benchmarks​

All benchmarks are configurable in one way or another, and `deepeval` offers an easy inferface to do so.

note

You'll notice although tasks and prompting techniques are configurable, scorers are not. This is because the type of scorer is an universal standard within any LLM benchmark.

### Tasks​

A task for an LLM benchmark is a challenge or problem is designed to assess an LLM's capabilities on a specific area of focus. For example, you can specify which **subset** of the the `MMLU` benchmark to evaluate your LLM on by providing a list of `MMLUTASK`:
    
    
    from deepeval.benchmarks import MMLU  
    from deepeval.benchmarks.task import MMLUTask  
      
    tasks = [MMLUTask.HIGH_SCHOOL_COMPUTER_SCIENCE, MMLUTask.ASTRONOMY]  
    benchmark = MMLU(tasks=tasks)  
    

In this example, we're only evaluating our Mistral 7B model on the MMLU `HIGH_SCHOOL_COMPUTER_SCIENCE` and `ASTRONOMY` tasks.

info

Each benchmark is associated with a unique **Task** enum which can be found on each benchmark's individual documentation pages. These tasks are 100% drawn from the original research papers for each respective benchmark, and maps one-to-one to the benchmark datasets available on Hugging Face.

By default, `deepeval` will evaluate your LLM on all available tasks for a particular benchmark.

### Few-Shot Learning​

Few-shot learning, also known as in-context learning, is a prompting technique that involves supplying your LLM a few examples as part of the prompt template to help its generation. These examples can help guide accuracy or behavior. The number of examples to provide, can be specified in the `n_shots` parameter:
    
    
    from deepeval.benchmarks import HellaSwag  
      
    benchmark = HellaSwag(n_shots=3)  
    

note

Each benchmark has a range of allowed `n_shots` values. `deepeval` handles all the logic with respect to the `n_shots` value according to the original research papers for each respective benchmark.

### CoTs Prompting​

Chain of thought prompting is an approach where the model is prompted to articulate its reasoning process to arrive at an answer. This usually results in an increase in prediction accuracy.
    
    
    from deepeval.benchmarks import BigBenchHard  
      
    benchmark = BigBenchHard(enable_cot=True)  
    

note

Not all benchmarks offers CoTs as a prompting technique, but the [original paper for BIG-Bench Hard](https://arxiv.org/abs/2210.09261) found major improvements when using CoTs prompting during benchmarking.

[Edit this page](https://github.com/confident-ai/deepeval/edit/main/docs/docs/benchmarks-introduction.mdx)

Last updated on **Apr 12, 2025** by **Jeffrey Ip**
