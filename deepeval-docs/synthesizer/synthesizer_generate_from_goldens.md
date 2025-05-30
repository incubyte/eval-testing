# Generate From Goldens

  * [](/)
  * Evaluation
  * Synthesizer
  * Generate from Goldens

On this page

# Generate From Goldens

DeepEval enables you to **generate synthetic Goldens from an existing set of Goldens** , without requiring any documents or context. This is ideal for quickly expanding or adding more complexity to your evaluation dataset.

![LangChain](https://confident-docs.s3.us-east-1.amazonaws.com/goldens_from_goldens.svg)

tip

By default, `generate_goldens_from_goldens` extracts `StylingConfig` from your existing Golden, but it is recommended to [provide a `StylingConfig` explicitly](/docs/synthesizer-introduction#styling-options) for better accuracy and consistency.

## Generate Your Goldens​

To get started, simply define a `Synthesizer` object and pass in your list of existing Goldens to the `generate_goldens_from_goldens` method.
    
    
    from deepeval.synthesizer import Synthesizer  
      
    synthesizer = Synthesizer()  
    synthesizer.generate_goldens_from_goldens(  
      goldens=goldens,  
      max_goldens_per_golden=2,  
      include_expected_output=True,  
    )  
    

There is **ONE** mandatory and **TWO** optional parameter when using the `generate_goldens_from_goldens` method:

  * `goldens`: a list of existing Goldens from which the new Goldens will be generated.
  * [Optional] `max_goldens_per_golden`: the maximum number of goldens to be generated per golden. Defaulted to 2.
  * [Optional] `include_expected_output`: a boolean which when set to `True`, will additionally generate an `expected_output` for each synthetic `Golden`. Defaulted to `True`.

info

If your existing Goldens include `context`, the synthesizer will utilize these contexts to generate synthetic Goldens, ensuring they are grounded in truth. If no context is present, the synthesizer will employ the `generate_from_scratch` method to create additional inputs based on provided inputs.

[Edit this page](https://github.com/confident-ai/deepeval/edit/main/docs/docs/synthesizer-generate-from-goldens.mdx)

Last updated on **Apr 14, 2025** by **Jeffrey Ip**
