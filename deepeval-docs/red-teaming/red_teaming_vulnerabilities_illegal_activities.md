# Illegal Activity

  * [](/)
  * Red-Teaming
  * Vulnerabilties
  * Illegal Activity

# Illegal Activity

The illegal activity vulnerability is designed to test whether an LLM can resist generating responses that facilitate or promote unlawful actions.
    
    
    pip install deepteam  
    
    
    
    from deepteam.vulnerabilities import IllegalActivity  
      
    illegal_activity = IllegalActivity(types=["violet crime"])  
    

Learn more how to red teaming LLM systesm using the illegal activity vulnerability on [DeepTeam's docs.](https://trydeepteam.com/docs/red-teaming-vulnerabilities-illegal-activity)

VERY IMPORTANT

We're making red teaming LLMs a much more dedicated experience and have created a new package specific for red teaming, called **DeepTeam**.

It is designed to be used within `deepeval`'s ecosystem (such as using custom models you're using for the metrics, using `deepeval`'s metrics for red teaming evaluation, etc.).

To begin, install `deepteam`:
    
    
    pip install deepteam  
    

You can read [DeepTeam's docs here.](https://trydeepteam.com/docs/red-teaming-vulnerabilities)

[Edit this page](https://github.com/confident-ai/deepeval/edit/main/docs/docs/red-teaming-vulnerabilities-illegal-activities.mdx)

Last updated on **Apr 12, 2025** by **Jeffrey Ip**
