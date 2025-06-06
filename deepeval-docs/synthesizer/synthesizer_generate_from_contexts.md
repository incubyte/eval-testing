# Generate From Contexts

  * [](/)
  * Evaluation
  * Synthesizer
  * Generate from Contexts

On this page

# Generate From Contexts

If you already have prepared contexts, you can skip document processing. Simply provide these contexts to the Synthesizer, and it will generate the Goldens directly without processing documents.

![LangChain](https://confident-bucket.s3.amazonaws.com/synthesize-from-contexts.svg)

tip

This is especially helpful if you **already have an embedded knowledge base**. For example, if you have documents parsed and stored in a vector database, you may handle retrieving text chunks yourself.

## Generate Your Goldens​

To generate synthetic `Golden`s from documents, simply provide a list of contexts:
    
    
    from deepeval.synthesizer import Synthesizer  
      
    synthesizer = Synthesizer()  
    synthesizer.generate_goldens_from_contexts(  
        # Provide a list of context for synthetic data generation  
        contexts=[  
            ["The Earth revolves around the Sun.", "Planets are celestial bodies."],  
            ["Water freezes at 0 degrees Celsius.", "The chemical formula for water is H2O."],  
        ]  
    )  
    

There are **ONE** mandatory and **THREE** optional parameters when using the `generate_goldens_from_contexts` method:

  * `contexts`: a list of context, where each context is itself a list of strings, ideally sharing a common theme or subject area.
  * [Optional] `include_expected_output`: a boolean which when set to `True`, will additionally generate an `expected_output` for each synthetic `Golden`. Defaulted to `True`.
  * [Optional] `max_goldens_per_context`: the maximum number of goldens to be generated per context. Defaulted to 2.
  * [Optional] `source_files`: a list of strings specifying the source of the contexts. Length of `source_files` **MUST** be the same as the length of `contexts`.

DID YOU KNOW?

The `generate_goldens_from_docs()` method calls the `generate_goldens_from_contexts()` method under the hood, and the only difference between the two is the `generate_goldens_from_contexts()` method does not contain a [context construction step](/docs/synthesizer-generate-from-docs#how-does-context-construction-work), but instead uses the provided contexts directly for generation.

[Edit this page](https://github.com/confident-ai/deepeval/edit/main/docs/docs/synthesizer-generate-from-contexts.mdx)

Last updated on **Apr 12, 2025** by **Jeffrey Ip**
