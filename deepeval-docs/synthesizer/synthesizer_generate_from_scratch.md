# Generate From Scratch

  * [](/)
  * Evaluation
  * Synthesizer
  * Generate from Scratch

On this page

# Generate From Scratch

You can also generate **synthetic Goldens from scratch** , without needing any documents or contexts.

![LangChain](https://confident-bucket.s3.amazonaws.com/synthesize-from-scratch.svg)

info

This approach is particularly useful if your LLM application **doesn't rely on RAG** or if you want to **test your LLM on queries beyond the existing knowledge base**.

## Generate Your Goldens​

Since there is no grounded context involved, you'll need to provide a `StylingConfig` when instantiating a `Synthesizer` for `deepeval`'s `Synthesizer` to know what types of goldens it should generate:
    
    
    from deepeval.synthesizer import Synthesizer  
    from deepeval.synthesizer.config import StylingConfig  
      
    styling_config = StylingConfig(  
      input_format="Questions in English that asks for data in database.",  
      expected_output_format="SQL query based on the given input",  
      task="Answering text-to-SQL-related queries by querying a database and returning the results to users"  
      scenario="Non-technical users trying to query a database using plain English.",  
    )  
      
    synthesizer = Synthesizer(styling_config=styling_config)  
    

Finally, to generate synthetic goldens without provided context, simply supply the number of goldens you want generated:
    
    
    from deepeval.synthesizer import Synthesizer  
      
    ...  
    synthesizer.generate_goldens_from_scratch(num_goldens=25)  
    print(synthesizer.synthetic_goldens)  
    

There is **ONE** mandatory parameter when using the `generate_goldens_from_scratch` method:

  * `num_goldens`: the number of goldens to generate.

[Edit this page](https://github.com/confident-ai/deepeval/edit/main/docs/docs/synthesizer-generate-from-scratch.mdx)

Last updated on **Apr 14, 2025** by **Jeffrey Ip**
