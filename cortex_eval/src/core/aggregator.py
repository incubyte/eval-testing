from typing import Dict, List, Any
import statistics
from collections import Counter


class ResultsAggregator:
    """Aggregates test results into summary statistics."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the results aggregator with configuration.
        
        Args:
            config: Dictionary containing aggregator configuration
        """
        self.config = config

    def aggregate_results(self, evaluated_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregate a list of evaluated test results.
        
        Args:
            evaluated_results: List of dictionaries containing evaluated test results
            
        Returns:
            Dictionary containing aggregated statistics
        """
        if not evaluated_results:
            return {
                'total_tests': 0,
                'metrics': {},
                'overall': {
                    'mean_score': 0,
                    'pass_rate': 0,
                }
            }

        # Extract scores for each metric
        metric_scores = {}
        for result in evaluated_results:
            eval_data = result.get('evaluation', {})
            metrics = eval_data.get('metrics', {})
            
            for metric_name, score in metrics.items():
                if metric_name not in metric_scores:
                    metric_scores[metric_name] = []
                metric_scores[metric_name].append(score)

        # Calculate statistics for each metric
        metrics_stats = {}
        for metric_name, scores in metric_scores.items():
            metrics_stats[metric_name] = {
                'mean': statistics.mean(scores),
                'median': statistics.median(scores),
                'min': min(scores),
                'max': max(scores),
                'std_dev': statistics.stdev(scores) if len(scores) > 1 else 0
            }

        # Calculate overall statistics
        overall_scores = [result.get('evaluation', {}).get('overall_score', 0) 
                          for result in evaluated_results]
        
        pass_count = sum(1 for result in evaluated_results 
                         if result.get('evaluation', {}).get('passed', False))

        # Response time statistics
        response_times = [result.get('response_time_ms', 0) for result in evaluated_results]

        # Categorize results by pass/fail and test category
        categories = Counter([result['test_case'].get('category', 'unknown') 
                              for result in evaluated_results])
        
        return {
            'total_tests': len(evaluated_results),
            'metrics': metrics_stats,
            'overall': {
                'mean_score': statistics.mean(overall_scores),
                'median_score': statistics.median(overall_scores),
                'pass_count': pass_count,
                'pass_rate': pass_count / len(evaluated_results),
                'response_time': {
                    'mean_ms': statistics.mean(response_times),
                    'median_ms': statistics.median(response_times),
                    'min_ms': min(response_times),
                    'max_ms': max(response_times)
                }
            },
            'categories': dict(categories)
        }