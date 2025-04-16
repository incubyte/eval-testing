from typing import List, Dict, Any, Optional
import os

from deepeval.synthesizer import Synthesizer as DeepEvalSynthesizer
from deepeval.dataset import EvaluationDataset


class DatasetGenerator:
    """
    Class for generating synthetic evaluation datasets using DeepEval.
    """
    
    def __init__(self):
        """
        Initialize the dataset generator with a DeepEval synthesizer.
        """
        self.synthesizer = DeepEvalSynthesizer()
    
    def generate_from_docs(self, 
                          document_paths: List[str], 
                          num_test_cases: int = 10, 
                          test_case_type: str = "rag") -> EvaluationDataset:
        """
        Generate synthetic test cases from document files.
        
        Args:
            document_paths: List of paths to document files
            num_test_cases: Number of test cases to generate
            test_case_type: Type of test cases to generate (rag, summarization, etc.)
            
        Returns:
            EvaluationDataset containing generated goldens
        """
        # Verify document paths exist
        for path in document_paths:
            if not os.path.exists(path):
                raise FileNotFoundError(f"Document not found: {path}")
        
        # Generate goldens using DeepEval synthesizer
        goldens = self.synthesizer.generate_goldens_from_docs(
            document_paths=document_paths,
            n=num_test_cases
        )
        
        return EvaluationDataset(goldens=goldens)
    
    def generate_from_contexts(self, 
                              contexts: List[str], 
                              num_test_cases: int = 10,
                              instruction: Optional[str] = None) -> EvaluationDataset:
        """
        Generate synthetic test cases from contexts.
        
        Args:
            contexts: List of context strings
            num_test_cases: Number of test cases to generate
            instruction: Optional instruction to guide generation
            
        Returns:
            EvaluationDataset containing generated goldens
        """
        # Generate goldens using DeepEval synthesizer
        goldens = self.synthesizer.generate_goldens_from_contexts(
            contexts=contexts,
            n=num_test_cases,
            instruction=instruction
        )
        
        return EvaluationDataset(goldens=goldens)
    
    def generate_from_scratch(self, 
                             topic: str, 
                             num_test_cases: int = 10,
                             instruction: Optional[str] = None) -> EvaluationDataset:
        """
        Generate synthetic test cases from scratch based on a topic.
        
        Args:
            topic: The topic to generate test cases for
            num_test_cases: Number of test cases to generate
            instruction: Optional instruction to guide generation
            
        Returns:
            EvaluationDataset containing generated goldens
        """
        # Generate goldens using DeepEval synthesizer
        goldens = self.synthesizer.generate_goldens_from_scratch(
            topic=topic,
            n=num_test_cases,
            instruction=instruction
        )
        
        return EvaluationDataset(goldens=goldens)