# Image Coherence

  * [](/)
  * Evaluation
  * Metrics
  * Multimodal Metrics
  * Image Coherence

On this page

# Image Coherence

The Image Coherence metric assesses the **coherent alignment of images with their accompanying text** , evaluating how effectively the visual content complements and enhances the textual narrative. `deepeval`'s Image Coherence metric is a self-explaining MLLM-Eval, meaning it outputs a reason for its metric score.

info

Image Coherence evaluates MLLM responses containing text accompanied by retrieved or generated images.

## Required Arguments​

To use the `ImageCoherence`, you'll have to provide the following arguments when creating a [`MLLMTestCase`](/docs/evaluation-test-cases#mllm-test-case):

  * `input`
  * `actual_output`

note

Remember that the `actual_output` of an `MLLMTestCase` is a list of strings and `Image` objects. If multiple images are provided in the actual output, The final score will be the average of each image's coherence.

The `input` and `actual_output` are required to create an `MLLMTestCase` (and hence required by all metrics) even though they might not be used for metric calculation. Read the How Is It Calculated section below to learn more.

## Example​
    
    
    from deepeval import evaluate  
    from deepeval.metrics import ImageCoherenceMetric  
    from deepeval.test_case import MLLMTestCase, MLLMImage  
      
    # Replace this with your actual MLLM application output  
    actual_output=[  
        "1. Take the sheet of paper and fold it lengthwise",  
        MLLMImage(url="./paper_plane_1", local=True),  
        "2. Unfold the paper. Fold the top left and right corners towards the center.",  
        MLLMImage(url="./paper_plane_2", local=True),  
        ...  
    ]  
      
    metric = ImageCoherenceMetric(  
        threshold=0.7,  
        include_reason=True,  
    )  
    test_case = MLLMTestCase(  
        input=["Provide step-by-step instructions on how to fold a paper airplane."],  
        actual_output=actual_output,  
    )  
      
    metric.measure(test_case)  
    print(metric.score)  
    print(metric.reason)  
      
    # or evaluate test cases in bulk  
    evaluate([test_case], [metric])  
    

There are **FIVE** optional parameters when creating a `ImageCoherence`:

  * [Optional] `threshold`: a float representing the minimum passing threshold, defaulted to 0.5.
  * [Optional] `strict_mode`: a boolean which when set to `True`, enforces a binary metric score: 1 for perfection, 0 otherwise. It also overrides the current threshold and sets it to 1. Defaulted to `False`.
  * [Optional] `async_mode`: a boolean which when set to `True`, enables [concurrent execution within the `measure()` method.](/docs/metrics-introduction#measuring-metrics-in-async) Defaulted to `True`.
  * [Optional] `verbose_mode`: a boolean which when set to `True`, prints the intermediate steps used to calculate said metric to the console, as outlined in the How Is It Calculated section. Defaulted to `False`.
  * [Optional] `max_context_size`: a number representing the maximum number of characters in each context, as outlined in the How Is It Calculated section. Defaulted to `None`.

## How Is It Calculated?​

The `ImageCoherence` score is calculated as follows:

  1. **Individual Image Coherence** : Each image's coherence score is based on the text directly above and below the image, limited by a `max_context_size` in characters. If `max_context_size` is not supplied, all available text is used. The equation can be expressed as:

Ci=f(Contextabove,Contextbelow,Imagei)C_i = f(\text{Context}_{\text{above}}, \text{Context}_{\text{below}}, \text{Image}_i)Ci​=f(Contextabove​,Contextbelow​,Imagei​)

  2. **Final Score** : The overall `ImageCoherence` score is the average of all individual image coherence scores for each image:

O=∑i=1nCinO = \frac{\sum_{i=1}^n C_i}{n}O=n∑i=1n​Ci​​

[Edit this page](https://github.com/confident-ai/deepeval/edit/main/docs/docs/multimodal-metrics-image-coherence.mdx)

Last updated on **Apr 12, 2025** by **Jeffrey Ip**
