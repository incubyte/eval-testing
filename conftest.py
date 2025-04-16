"""
This file sets up pytest configuration for DeepEval tests.
"""

import os
import pytest
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create results directory if it doesn't exist
if not os.path.exists("results"):
    os.makedirs("results")