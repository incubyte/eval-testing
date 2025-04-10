import os
import json
import logging
from typing import Dict, Any, Optional
import datetime


class DashboardGenerator:
    """Generates HTML dashboard for test results."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the dashboard generator with configuration.
        
        Args:
            config: Dictionary containing dashboard configuration
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Set defaults
        self.template_path = config.get('template_path', './src/reporting/templates/dashboard.html')
        self.output_path = config.get('output_path', './reports/dashboard.html')
        self.include_charts = config.get('include_charts', True)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

    def generate(self, aggregated_results: Dict[str, Any]) -> str:
        """
        Generate dashboard HTML from aggregated results.
        
        Args:
            aggregated_results: Dictionary containing aggregated test results
            
        Returns:
            Path to the generated dashboard HTML file
        """
        if not aggregated_results:
            self.logger.warning("No results to generate dashboard")
            return ""
            
        # If template exists, use it, otherwise generate from scratch
        if os.path.exists(self.template_path):
            html = self._render_template(aggregated_results)
        else:
            self.logger.warning(f"Template not found at {self.template_path}, generating basic dashboard")
            html = self._generate_basic_dashboard(aggregated_results)
            
        # Write dashboard to file
        try:
            with open(self.output_path, 'w', encoding='utf-8') as f:
                f.write(html)
                
            self.logger.info(f"Dashboard generated at {self.output_path}")
            return self.output_path
        except Exception as e:
            self.logger.error(f"Error writing dashboard: {str(e)}")
            return ""

    def _render_template(self, results: Dict[str, Any]) -> str:
        """
        Render dashboard using HTML template.
        
        Args:
            results: Dictionary containing aggregated test results
            
        Returns:
            String containing the rendered HTML
        """
        try:
            with open(self.template_path, 'r', encoding='utf-8') as f:
                template = f.read()
                
            # Convert results to JSON for embedding in template
            results_json = json.dumps(results)
            
            # Replace placeholders
            html = template.replace('{{RESULTS_JSON}}', results_json)
            html = html.replace('{{TIMESTAMP}}', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            html = html.replace('{{TOTAL_TESTS}}', str(results.get('total_tests', 0)))
            html = html.replace('{{PASS_RATE}}', f"{results.get('overall', {}).get('pass_rate', 0) * 100:.1f}%")
            
            return html
        except Exception as e:
            self.logger.error(f"Error rendering template: {str(e)}")
            return self._generate_basic_dashboard(results)

    def _generate_basic_dashboard(self, results: Dict[str, Any]) -> str:
        """
        Generate basic dashboard HTML from scratch.
        
        Args:
            results: Dictionary containing aggregated test results
            
        Returns:
            String containing the generated HTML
        """
        # Extract metrics
        total_tests = results.get('total_tests', 0)
        overall = results.get('overall', {})
        pass_rate = overall.get('pass_rate', 0) * 100
        mean_score = overall.get('mean_score', 0) * 100
        metrics = results.get('metrics', {})
        
        # Generate dashboard HTML
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cortex Evaluation Dashboard</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
        .header {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        .summary {{ display: flex; justify-content: space-between; margin-bottom: 20px; }}
        .summary-card {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; flex: 1; margin: 0 10px; text-align: center; }}
        .summary-card:first-child {{ margin-left: 0; }}
        .summary-card:last-child {{ margin-left: 0; }}
        .metric-value {{ font-size: 24px; font-weight: bold; margin: 10px 0; }}
        .metrics-table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        .metrics-table th, .metrics-table td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        .metrics-table th {{ background-color: #f2f2f2; }}
        .chart-container {{ margin-top: 30px; height: 400px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Cortex Evaluation Dashboard</h1>
        <p>Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="summary">
        <div class="summary-card">
            <h3>Total Tests</h3>
            <div class="metric-value">{total_tests}</div>
        </div>
        <div class="summary-card">
            <h3>Pass Rate</h3>
            <div class="metric-value">{pass_rate:.1f}%</div>
        </div>
        <div class="summary-card">
            <h3>Mean Score</h3>
            <div class="metric-value">{mean_score:.1f}%</div>
        </div>
    </div>
    
    <h2>Metrics Breakdown</h2>
    <table class="metrics-table">
        <tr>
            <th>Metric</th>
            <th>Mean</th>
            <th>Median</th>
            <th>Min</th>
            <th>Max</th>
        </tr>
"""
        
        # Add rows for each metric
        for metric_name, metric_data in metrics.items():
            html += f"""
        <tr>
            <td>{metric_name}</td>
            <td>{metric_data.get('mean', 0) * 100:.1f}%</td>
            <td>{metric_data.get('median', 0) * 100:.1f}%</td>
            <td>{metric_data.get('min', 0) * 100:.1f}%</td>
            <td>{metric_data.get('max', 0) * 100:.1f}%</td>
        </tr>"""
        
        html += """
    </table>
"""
        
        # Add charts if enabled
        if self.include_charts:
            html += """
    <div class="chart-container">
        <h2>Performance Visualization</h2>
        <canvas id="metricsChart"></canvas>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        // Parse result data
        const results = """
            html += json.dumps(results)
            html += """;
        
        // Set up metrics chart
        const ctx = document.getElementById('metricsChart').getContext('2d');
        
        const metricNames = Object.keys(results.metrics);
        const metricMeans = metricNames.map(name => results.metrics[name].mean * 100);
        
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: metricNames,
                datasets: [{
                    label: 'Mean Score (%)',
                    data: metricMeans,
                    backgroundColor: 'rgba(54, 162, 235, 0.5)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    </script>
"""
        
        html += """
</body>
</html>
"""
        
        return html
        
    def export_data_for_external_dashboard(self, results: Dict[str, Any], output_path: Optional[str] = None) -> str:
        """
        Export data in JSON format for use in external dashboards.
        
        Args:
            results: Dictionary containing aggregated test results
            output_path: Optional path to write the data
            
        Returns:
            Path to the exported data file
        """
        if not output_path:
            output_path = os.path.join(os.path.dirname(self.output_path), 'dashboard_data', 
                                     f"results_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.json")
                                     
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2)
                
            self.logger.info(f"Dashboard data exported to {output_path}")
            return output_path
        except Exception as e:
            self.logger.error(f"Error exporting dashboard data: {str(e)}")
            return ""