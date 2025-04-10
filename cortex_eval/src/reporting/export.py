import json
import csv
import logging
import os
from typing import Dict, List, Any, Optional
import datetime


class ResultsExporter:
    """Exports evaluation results to various formats."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the results exporter with configuration.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Set default export directory
        self.export_dir = self.config.get('export_dir', './reports/exports')
        os.makedirs(self.export_dir, exist_ok=True)

    def export_to_json(self, results: Dict[str, Any], output_path: Optional[str] = None) -> str:
        """
        Export results to a JSON file.
        
        Args:
            results: Dictionary containing results to export
            output_path: Optional path to write the JSON file
            
        Returns:
            Path to the exported JSON file
        """
        if not output_path:
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            output_path = os.path.join(self.export_dir, f"results_{timestamp}.json")
            
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2)
                
            self.logger.info(f"Results exported to JSON: {output_path}")
            return output_path
        except Exception as e:
            self.logger.error(f"Error exporting to JSON: {str(e)}")
            return ""

    def export_to_csv(self, results: List[Dict[str, Any]], output_path: Optional[str] = None) -> str:
        """
        Export test results to a CSV file.
        
        Args:
            results: List of test result dictionaries
            output_path: Optional path to write the CSV file
            
        Returns:
            Path to the exported CSV file
        """
        if not results:
            self.logger.warning("No results to export to CSV")
            return ""
            
        if not output_path:
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            output_path = os.path.join(self.export_dir, f"results_{timestamp}.csv")
            
        try:
            # Determine CSV columns based on first result
            first_result = results[0]
            test_case = first_result.get('test_case', {})
            evaluation = first_result.get('evaluation', {})
            metrics = evaluation.get('metrics', {})
            
            # Define main columns
            columns = [
                'test_id', 'question', 'ground_truth', 'response', 
                'response_time_ms', 'passed', 'overall_score'
            ]
            
            # Add metric columns
            metric_columns = [f"metric_{name}" for name in metrics.keys()]
            columns.extend(metric_columns)
            
            with open(output_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=columns)
                writer.writeheader()
                
                for result in results:
                    test_case = result.get('test_case', {})
                    evaluation = result.get('evaluation', {})
                    metrics = evaluation.get('metrics', {})
                    
                    row = {
                        'test_id': test_case.get('id', 'unknown'),
                        'question': test_case.get('question', ''),
                        'ground_truth': test_case.get('ground_truth', ''),
                        'response': self._get_response_text(result.get('response', {})),
                        'response_time_ms': result.get('response_time_ms', 0),
                        'passed': evaluation.get('passed', False),
                        'overall_score': evaluation.get('overall_score', 0)
                    }
                    
                    # Add metric scores
                    for name, value in metrics.items():
                        row[f"metric_{name}"] = value
                        
                    writer.writerow(row)
                    
            self.logger.info(f"Results exported to CSV: {output_path}")
            return output_path
        except Exception as e:
            self.logger.error(f"Error exporting to CSV: {str(e)}")
            return ""

    def export_summary_to_markdown(self, aggregated_results: Dict[str, Any], 
                                 output_path: Optional[str] = None) -> str:
        """
        Export a summary of aggregated results to Markdown.
        
        Args:
            aggregated_results: Dictionary containing aggregated results
            output_path: Optional path to write the Markdown file
            
        Returns:
            Path to the exported Markdown file
        """
        if not aggregated_results:
            self.logger.warning("No aggregated results to export")
            return ""
            
        if not output_path:
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            output_path = os.path.join(self.export_dir, f"summary_{timestamp}.md")
            
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                # Write header
                f.write("# Cortex Evaluation Summary\n\n")
                f.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                # Overall statistics
                total_tests = aggregated_results.get('total_tests', 0)
                overall = aggregated_results.get('overall', {})
                pass_count = overall.get('pass_count', 0)
                pass_rate = overall.get('pass_rate', 0) * 100
                mean_score = overall.get('mean_score', 0) * 100
                
                f.write("## Overall Results\n\n")
                f.write(f"- **Total Tests**: {total_tests}\n")
                f.write(f"- **Passing Tests**: {pass_count}\n")
                f.write(f"- **Pass Rate**: {pass_rate:.1f}%\n")
                f.write(f"- **Mean Score**: {mean_score:.1f}%\n\n")
                
                # Metrics breakdown
                metrics = aggregated_results.get('metrics', {})
                f.write("## Metrics Breakdown\n\n")
                f.write("| Metric | Mean | Median | Min | Max |\n")
                f.write("|--------|------|--------|-----|-----|\n")
                
                for name, data in metrics.items():
                    mean = data.get('mean', 0) * 100
                    median = data.get('median', 0) * 100
                    min_val = data.get('min', 0) * 100
                    max_val = data.get('max', 0) * 100
                    
                    f.write(f"| {name} | {mean:.1f}% | {median:.1f}% | {min_val:.1f}% | {max_val:.1f}% |\n")
                    
                f.write("\n")
                
                # Category breakdown if available
                categories = aggregated_results.get('categories', {})
                if categories:
                    f.write("## Categories\n\n")
                    f.write("| Category | Count |\n")
                    f.write("|----------|-------|\n")
                    
                    for category, count in categories.items():
                        f.write(f"| {category} | {count} |\n")
                
                # Response times
                response_times = overall.get('response_time', {})
                if response_times:
                    f.write("\n## Response Times\n\n")
                    f.write(f"- **Mean**: {response_times.get('mean_ms', 0):.1f} ms\n")
                    f.write(f"- **Median**: {response_times.get('median_ms', 0):.1f} ms\n")
                    f.write(f"- **Min**: {response_times.get('min_ms', 0):.1f} ms\n")
                    f.write(f"- **Max**: {response_times.get('max_ms', 0):.1f} ms\n")
                
            self.logger.info(f"Summary exported to Markdown: {output_path}")
            return output_path
        except Exception as e:
            self.logger.error(f"Error exporting summary to Markdown: {str(e)}")
            return ""

    def _get_response_text(self, response: Dict[str, Any]) -> str:
        """
        Extract text from a response dictionary.
        
        Args:
            response: Response dictionary
            
        Returns:
            Response text
        """
        # Try different common fields
        if 'text' in response:
            return response['text']
        elif 'answer' in response:
            return response['answer']
        elif 'content' in response:
            return response['content']
        elif 'message' in response and 'content' in response['message']:
            return response['message']['content']
        else:
            # Return empty string if no text field found
            return ""