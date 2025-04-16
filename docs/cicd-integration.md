# CI/CD Integration Guide

This guide explains how to integrate the LLM evaluation framework with Azure DevOps CI/CD pipelines.

## Overview

The framework provides Azure DevOps pipeline definitions that can:

1. Run LLM evaluations as part of your CI/CD pipeline
2. Store evaluation results as build artifacts
3. Analyze results and determine if they meet quality thresholds
4. Notify teams about evaluation results
5. Pass/fail builds based on evaluation thresholds

## Setup

### 1. Create Azure Resources

First, set up the required Azure resources:

```bash
# Login to Azure
az login

# Create resource group
az group create --name llm-eval-resources --location eastus

# Create storage account for results
az storage account create \
    --name llmevalresults \
    --resource-group llm-eval-resources \
    --location eastus \
    --sku Standard_LRS

# Create Key Vault for secrets
az keyvault create \
    --name llm-eval-keys \
    --resource-group llm-eval-resources \
    --location eastus

# Store API keys in Key Vault
az keyvault secret set \
    --vault-name llm-eval-keys \
    --name OPENAI-API-KEY \
    --value "your-openai-api-key"

az keyvault secret set \
    --vault-name llm-eval-keys \
    --name ROLAI-AUTH-TOKEN \
    --value "your-rolai-auth-token"

# Create App Service for review UI (optional)
az appservice plan create \
    --name llm-eval-plan \
    --resource-group llm-eval-resources \
    --sku B1 \
    --is-linux

az webapp create \
    --name llm-eval-review-app \
    --resource-group llm-eval-resources \
    --plan llm-eval-plan \
    --runtime "PYTHON|3.12"
```

### 2. Configure Azure DevOps

1. Create a service connection to Azure:
   - Go to Project Settings > Service connections > New service connection
   - Select Azure Resource Manager
   - Choose Service Principal (automatic)
   - Select your subscription and resource group
   - Name it "llm-eval-azure"

2. Set pipeline variables:
   - Create a variable group named "llm-eval-variables"
   - Add the following variables:
     - ROLAI_BASE_URL
     - ROLAI_ORGANIZATION_ID
     - Config path (if different from default)

3. Import the pipeline:
   - Go to Pipelines > New pipeline
   - Select Azure Repos Git (or your repo provider)
   - Select your repository
   - Select "Existing Azure Pipelines YAML file"
   - Enter the path: `/azure-pipelines/llm-eval.yml`
   - Review and save the pipeline

## Pipeline Configuration

### Basic Pipeline

The basic pipeline runs evaluations on changes to test cases or source code:

```yaml
trigger:
  branches:
    include:
      - main
      - develop
  paths:
    include:
      - 'test_cases/**'
      - 'config/**'
      - 'src/**'

pool:
  vmImage: 'ubuntu-latest'

variables:
  pythonVersion: '3.12'
  configFile: '$(Build.SourcesDirectory)/config/default.yaml'
  resultsDir: '$(Build.ArtifactStagingDirectory)/evaluation-results'

stages:
- stage: Evaluation
  displayName: 'LLM Evaluation'
  jobs:
  - job: RunEvaluation
    displayName: 'Run Evaluations'
    steps:
    # Setup and run evaluations
    # ...
```

### Scheduled Evaluations

To run evaluations on a schedule:

```yaml
schedules:
- cron: "0 0 * * *"  # Run daily at midnight
  displayName: Daily evaluation
  branches:
    include:
    - main
  always: true  # Run even if no code changes
```

### Pull Request Validation

To run evaluations on pull requests:

```yaml
trigger: none  # Disable CI trigger

pr:
  branches:
    include:
      - main
      - develop
  paths:
    include:
      - 'test_cases/**'
      - 'config/**'
      - 'src/**'
```

## Notification Integration

The pipeline can send notifications via Azure Functions:

1. Create an Azure Function for notifications
2. Configure the function URL and key in your pipeline
3. The pipeline will send evaluation results to the function
4. The function can send emails, post to Teams/Slack, etc.

## Evaluation Thresholds

The pipeline can fail if evaluations don't meet quality thresholds:

```yaml
- script: |
    # Check for failing tests with 70% threshold
    python -m src.cli.analyze --results $(System.ArtifactsDirectory)/evaluation-results --threshold 0.7
  displayName: 'Analyze results'
  failOnStderr: true  # Fail if threshold not met
```

## Debugging

If your pipeline fails, check:

1. Build logs for error messages
2. That all required secrets are available in Key Vault
3. That service connections have appropriate permissions
4. That evaluation thresholds are appropriate for your use case

## Next Steps

Consider implementing:

1. A web UI for reviewing evaluation results
2. Integration with your bug tracking system
3. Dashboards for tracking evaluation metrics over time
4. Automated retraining of models that fail evaluations