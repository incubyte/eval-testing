import sqlite3
import json
import logging
import os
from typing import Dict, List, Any, Optional
import datetime


class ResultsDatabase:
    """Stores and retrieves evaluation results in a database."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the results database with configuration.
        
        Args:
            config: Dictionary containing database configuration
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        db_type = config.get('type', 'sqlite')
        if db_type != 'sqlite':
            self.logger.warning(f"Database type {db_type} not supported, using sqlite")
            
        self.db_path = config.get('path', './reports/results.db')
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # Initialize database
        self._initialize_db()

    def _initialize_db(self) -> None:
        """
        Initialize the database schema if it doesn't exist.
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create tables if they don't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS test_runs (
                    run_id TEXT PRIMARY KEY,
                    timestamp TEXT,
                    service_type TEXT,
                    dataset_path TEXT,
                    config TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS test_results (
                    result_id TEXT PRIMARY KEY,
                    run_id TEXT,
                    test_id TEXT,
                    question TEXT,
                    response TEXT,
                    ground_truth TEXT,
                    response_time_ms REAL,
                    timestamp TEXT,
                    evaluation TEXT,
                    FOREIGN KEY (run_id) REFERENCES test_runs (run_id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS aggregated_results (
                    run_id TEXT PRIMARY KEY,
                    total_tests INTEGER,
                    pass_count INTEGER,
                    pass_rate REAL,
                    mean_score REAL,
                    results_json TEXT,
                    FOREIGN KEY (run_id) REFERENCES test_runs (run_id)
                )
            ''')
            
            conn.commit()
            self.logger.info("Database initialized successfully")
        except sqlite3.Error as e:
            self.logger.error(f"Database initialization error: {str(e)}")
        finally:
            if conn:
                conn.close()

    def store_results(self, evaluated_results: List[Dict[str, Any]], 
                     run_metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Store evaluated test results in the database.
        
        Args:
            evaluated_results: List of evaluated test result dictionaries
            run_metadata: Optional metadata for the test run
            
        Returns:
            String run_id for the stored results
        """
        if not evaluated_results:
            self.logger.warning("No results to store")
            return ""
            
        run_id = run_metadata.get('run_id') if run_metadata else self._generate_run_id()
        
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Store run metadata
            metadata = run_metadata or {}
            timestamp = metadata.get('timestamp', datetime.datetime.now().isoformat())
            service_type = metadata.get('service_type', 'unknown')
            dataset_path = metadata.get('dataset_path', 'unknown')
            config_json = json.dumps(metadata.get('config', {}))
            
            cursor.execute(
                'INSERT OR REPLACE INTO test_runs VALUES (?, ?, ?, ?, ?)',
                (run_id, timestamp, service_type, dataset_path, config_json)
            )
            
            # Store individual test results
            for result in evaluated_results:
                result_id = self._generate_result_id(run_id, result)
                test_case = result.get('test_case', {})
                test_id = test_case.get('id', 'unknown')
                question = test_case.get('question', '')
                ground_truth = test_case.get('ground_truth', '')
                response = json.dumps(result.get('response', {}))
                response_time_ms = result.get('response_time_ms', 0)
                timestamp = result.get('timestamp', datetime.datetime.now().isoformat())
                evaluation = json.dumps(result.get('evaluation', {}))
                
                cursor.execute(
                    'INSERT OR REPLACE INTO test_results VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (result_id, run_id, test_id, question, response, ground_truth, 
                     response_time_ms, timestamp, evaluation)
                )
            
            conn.commit()
            self.logger.info(f"Stored {len(evaluated_results)} test results with run_id {run_id}")
            return run_id
            
        except sqlite3.Error as e:
            self.logger.error(f"Error storing results: {str(e)}")
            return ""
        finally:
            if conn:
                conn.close()

    def store_aggregated_results(self, aggregated_results: Dict[str, Any], 
                                run_id: Optional[str] = None) -> None:
        """
        Store aggregated test results in the database.
        
        Args:
            aggregated_results: Dictionary containing aggregated results
            run_id: Optional run_id to associate with these results
        """
        if not aggregated_results:
            self.logger.warning("No aggregated results to store")
            return
            
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Use provided run_id or extract from aggregated results
            result_run_id = run_id or aggregated_results.get('run_id', self._generate_run_id())
            
            # Extract key metrics
            total_tests = aggregated_results.get('total_tests', 0)
            pass_count = aggregated_results.get('overall', {}).get('pass_count', 0)
            pass_rate = aggregated_results.get('overall', {}).get('pass_rate', 0)
            mean_score = aggregated_results.get('overall', {}).get('mean_score', 0)
            results_json = json.dumps(aggregated_results)
            
            cursor.execute(
                'INSERT OR REPLACE INTO aggregated_results VALUES (?, ?, ?, ?, ?, ?)',
                (result_run_id, total_tests, pass_count, pass_rate, mean_score, results_json)
            )
            
            conn.commit()
            self.logger.info(f"Stored aggregated results for run_id {result_run_id}")
            
        except sqlite3.Error as e:
            self.logger.error(f"Error storing aggregated results: {str(e)}")
        finally:
            if conn:
                conn.close()

    def get_test_results(self, run_id: str = None, 
                        limit: int = 100, 
                        offset: int = 0) -> List[Dict[str, Any]]:
        """
        Retrieve test results from the database.
        
        Args:
            run_id: Optional run_id to filter results
            limit: Maximum number of results to return
            offset: Number of results to skip
            
        Returns:
            List of test result dictionaries
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = '''
                SELECT * FROM test_results
            '''
            
            params = []
            if run_id:
                query += ' WHERE run_id = ?'
                params.append(run_id)
                
            query += ' ORDER BY timestamp DESC LIMIT ? OFFSET ?'
            params.extend([limit, offset])
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            results = []
            for row in rows:
                result = dict(row)
                # Parse JSON fields
                result['response'] = json.loads(result['response'])
                result['evaluation'] = json.loads(result['evaluation'])
                results.append(result)
                
            return results
            
        except sqlite3.Error as e:
            self.logger.error(f"Error retrieving results: {str(e)}")
            return []
        finally:
            if conn:
                conn.close()

    def get_aggregated_results(self, run_id: str = None) -> Dict[str, Any]:
        """
        Retrieve aggregated results from the database.
        
        Args:
            run_id: Optional run_id to filter results
            
        Returns:
            Dictionary containing aggregated results, or empty dict if not found
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = '''
                SELECT * FROM aggregated_results
            '''
            
            params = []
            if run_id:
                query += ' WHERE run_id = ?'
                params.append(run_id)
            else:
                query += ' ORDER BY total_tests DESC LIMIT 1'
                
            cursor.execute(query, params)
            row = cursor.fetchone()
            
            if row:
                result = dict(row)
                # Parse JSON fields
                result['results_json'] = json.loads(result['results_json'])
                return result
            else:
                return {}
                
        except sqlite3.Error as e:
            self.logger.error(f"Error retrieving aggregated results: {str(e)}")
            return {}
        finally:
            if conn:
                conn.close()

    def _generate_run_id(self) -> str:
        """
        Generate a unique run ID.
        
        Returns:
            String run ID
        """
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        return f"run_{timestamp}_{unique_id}"

    def _generate_result_id(self, run_id: str, result: Dict[str, Any]) -> str:
        """
        Generate a unique result ID.
        
        Args:
            run_id: Run ID for this result
            result: Result dictionary
            
        Returns:
            String result ID
        """
        test_case = result.get('test_case', {})
        test_id = test_case.get('id', 'unknown')
        import hashlib
        hash_input = f"{run_id}_{test_id}"
        return f"result_{hashlib.md5(hash_input.encode()).hexdigest()[:12]}"