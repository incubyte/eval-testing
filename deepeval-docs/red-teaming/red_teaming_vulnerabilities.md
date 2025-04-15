# Introduction

  * [](/)
  * Red Teaming
  * Vulnerabilties
  * Introduction

On this page

# Introduction

## Quick Summary​

Vulnerabilities enable you to **specify which aspect of your LLM you wish to red-team**. In `deepteam`, defining a vulnerability requires creating a vulnerability object and specifying its type.
    
    
    from deepteam.vulnerabilities import PIILeakage, Bias  
      
    pii_leakage = PIILeakage(types=["direct disclosure"])  
    bias = Bias(type=["race"])  
    

info

Each vulnerability accepts a `types` parameter that accepts a list of strings specific to that vulnerability. For example, `Bias` accepts "race", "gender", "political", and "religion" as `types`.

To use your defined vulnerabilities, supply it to the `red_team()` method:
    
    
    from deepteam import red_team  
    ...  
      
    red_team(vulnerabilities[pii_leakage, bias], model_callback=..., attacks=[...])  
    

`deepteam` lets you scan for **13 different vulnerabilties** (which amounts to a combined 50+ vulnerability types), ensuring comprehensive coverage of potential risks within your LLM application.

These risks and vulnerabilities include:

  * **Data Privacy**
    * [PII Leakage](/docs/red-teaming-vulnerabilities-pii-leakage)
    * [Prompt Leakage](/docs/red-teaming-vulnerabilities-prompt-leakage)
  * **Responsible AI**
    * [Bias](/docs/red-teaming-vulnerabilities-bias)
    * [Toxicity](/docs/red-teaming-vulnerabilities-toxicity)
  * **Unauthorized Access**
    * [Unauthorized Access](/docs/red-teaming-vulnerabilities-unauthorized-access)
  * **Brand Image**
    * [Misinformation](/docs/red-teaming-vulnerabilities-misinformation)
    * [Intellectual Property](/docs/red-teaming-vulnerabilities-intellectual-property)
    * [ExcessiveAgency](/docs/red-teaming-vulnerabilities-excessive-agency)
    * [Robustnesss](/docs/red-teaming-vulnerabilities-robustness)
    * [Competition](/docs/red-teaming-vulnerabilities-competition)
  * **Illegal Risks**
    * [Illegal Activities](/docs/red-teaming-vulnerabilities-illegal-activities)
    * [Graphic Content](/docs/red-teaming-vulnerabilities-graphic-content)
    * [Personal Safety](/docs/red-teaming-vulnerabilities-personal-safety)

## Five Main LLM Risks​

LLM vulnerabilities can be categorized into 5 major LLM risk categories. Think of these categories simply as collections of vulnerabilities.

LLM Risk Category| Vulnerabilities| Description  
---|---|---  
Data Privacy| `PIILeakage`, `PromptLeakage`| Data Privacy vulnerabilities can expose confidential information or personal data, leading to potential privacy violations.  
Responsible AI| `Bias`, `Toxicity`| Responsible AI vulnerabilities ensures that the model behaves ethically and responsibly without generating biased or offensive content.  
Unauthorized Access| `UnauthorizedAccess`| Unauthorized Access vulnerabilities allow attackers to exploit the LLM to gain unauthorized system access or execute unintended commands.  
Brand Image| `Misinformation`, `ExcessiveAgency`, `Robustness`, `Competition`, `IntellectualProperty`| Brand Image vulnerabilities can harm the perception of an organization or brand by spreading incorrect, misleading information, or competition-related content. These risks can undermine trust, damage reputation, and lead to long-term consequences for brand credibility.  
Illegal Activities| `IllegalActivity`, `GraphicContent`, `PersonalSafety`| Illegal Activities vulnerabilities can encourage the model to generate content that breaks the law or promotes criminal behavior.  
  
[Edit this page](https://github.com/confident-ai/deepteam/edit/main/docs/docs/red-teaming-vulnerabilities.mdx)

Last updated on **Apr 3, 2025** by **penguine**
