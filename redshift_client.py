import os
import pandas as pd
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, Dict, List, Union

load_dotenv()

class RedshiftClient:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self._connect()

    def _connect(self):
        """Establish connection to Redshift"""
        try:
            self.conn = psycopg2.connect(
                dbname=os.getenv('REDSHIFT_DATABASE'),
                user=os.getenv('REDSHIFT_USER'),
                password=os.getenv('REDSHIFT_PASSWORD'),
                host=os.getenv('REDSHIFT_HOST'),
                port=os.getenv('REDSHIFT_PORT', '5439')
            )
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Redshift: {str(e)}")

    def execute_query(self, query: str, params: Optional[Dict] = None) -> List[Dict]:
        """
        Execute a query and return results as a list of dictionaries
        
        Args:
            query: SQL query string
            params: Optional parameters for parameterized queries
            
        Returns:
            List of dictionaries containing query results
        """
        try:
            self.cursor.execute(query, params)
            results = self.cursor.fetchall()
            return [dict(row) for row in results]
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Query execution failed: {str(e)}")

    def query_to_dataframe(self, query: str, params: Optional[Dict] = None) -> pd.DataFrame:
        """
        Execute a query and return results as a pandas DataFrame
        
        Args:
            query: SQL query string
            params: Optional parameters for parameterized queries
            
        Returns:
            pandas DataFrame containing query results
        """
        results = self.execute_query(query, params)
        return pd.DataFrame(results)

    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def run_query(query: str, params: Optional[Dict] = None, output_format: str = 'dict') -> Union[List[Dict], pd.DataFrame]:
    """
    Helper function to run a query and return results
    
    Args:
        query: SQL query string
        params: Optional parameters for parameterized queries
        output_format: 'dict' for list of dictionaries or 'df' for pandas DataFrame
        
    Returns:
        Query results in specified format
    """
    with RedshiftClient() as client:
        if output_format == 'df':
            return client.query_to_dataframe(query, params)
        return client.execute_query(query, params) 