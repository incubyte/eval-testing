import json
import os
from typing import Dict, Any, List
from datetime import datetime


class ResultHandler:
    """
    Utility class for saving and loading evaluation results.
    """
    
    @staticmethod
    def save_results(results: List[Dict[str, Any]], output_dir: str, filename: str = None) -> str:
        """
        Save evaluation results to a JSON file.
        
        Args:
            results: The evaluation results to save
            output_dir: Directory to save the results in
            filename: Optional filename, defaults to timestamp-based name
            
        Returns:
            Path to the saved file
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"evaluation_results_{timestamp}.json"
        
        # Ensure filename has .json extension
        if not filename.endswith('.json'):
            filename += '.json'
        
        # Full path to output file
        file_path = os.path.join(output_dir, filename)
        
        # Save results to file
        with open(file_path, 'w') as file:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "results": results
            }, file, indent=2)
        
        return file_path
    
    @staticmethod
    def load_results(file_path: str) -> Dict[str, Any]:
        """
        Load evaluation results from a JSON file.
        
        Args:
            file_path: Path to the results file
            
        Returns:
            Dictionary containing evaluation results
            
        Raises:
            FileNotFoundError: If the file does not exist
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Results file not found: {file_path}")
        
        with open(file_path, 'r') as file:
            return json.load(file)