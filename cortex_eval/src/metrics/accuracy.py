from typing import Dict, Any
import nltk
import logging
from nltk.tokenize import word_tokenize
from nltk.translate.bleu_score import sentence_bleu
import importlib.util


class AccuracyMetric:
    """Measures factual accuracy of responses compared to ground truth."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the accuracy metric with configuration.
        
        Args:
            config: Dictionary containing metric configuration
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Check if Rouge is available, otherwise fallback to simpler metrics
        self.rouge_available = importlib.util.find_spec("rouge") is not None
        if self.rouge_available:
            try:
                from rouge import Rouge
                self.rouge = Rouge()
            except ImportError:
                self.rouge_available = False
                self.logger.warning("Rouge package not properly installed, falling back to simpler metrics")
        else:
            self.logger.warning("Rouge package not available, falling back to simpler metrics")

        # Ensure NLTK dependencies are downloaded
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            self.logger.info("Downloading NLTK punkt tokenizer")
            nltk.download('punkt', quiet=True)

    def calculate(self, response: Dict[str, Any], ground_truth: str, test_case: Dict[str, Any]) -> float:
        """
        Calculate accuracy score using multiple NLP metrics.
        
        Args:
            response: Dictionary containing the service response
            ground_truth: String containing the expected correct answer
            test_case: Dictionary containing the test case data
            
        Returns:
            Float between 0 and 1 representing accuracy score
        """
        # Extract response text
        response_text = response.get('text', '')
        if not response_text and 'answer' in response:
            response_text = response.get('answer', '')
            
        if not response_text:
            self.logger.warning(f"Empty response for test case {test_case.get('id', 'unknown')}")
            return 0.0

        # Calculate BLEU score (n-gram precision)
        try:
            reference_tokens = [word_tokenize(ground_truth)]
            hypothesis_tokens = word_tokenize(response_text)
            bleu_score = sentence_bleu(reference_tokens, hypothesis_tokens)
        except Exception as e:
            self.logger.warning(f"BLEU calculation failed: {str(e)}")
            bleu_score = 0.0

        # Calculate ROUGE scores (recall-oriented) if available
        rouge_l_score = 0.0
        if self.rouge_available:
            try:
                rouge_scores = self.rouge.get_scores(response_text, ground_truth)[0]
                rouge_l_score = rouge_scores['rouge-l']['f']
            except Exception as e:
                self.logger.warning(f"ROUGE calculation failed: {str(e)}")
                rouge_l_score = 0.0

        # Combine scores (can be weighted based on config)
        bleu_weight = self.config.get('bleu_weight', 0.5)
        rouge_weight = self.config.get('rouge_weight', 0.5)

        if not self.rouge_available:
            # If Rouge is not available, use BLEU score with higher weight
            combined_score = bleu_score
        else:
            combined_score = (bleu_score * bleu_weight) + (rouge_l_score * rouge_weight)
            
        return max(0.0, min(1.0, combined_score))  # Ensure score is between 0 and 1