import os
import pandas as pd
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, Dict, List, Union
import re

load_dotenv()

class RedshiftClient:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self._connect()
        self.schema_cache = {}
        self.table_cache = None

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

    def get_available_tables(self, schema: str = 'cc') -> List[str]:
        """
        Get list of available tables in the specified schema
        
        Args:
            schema: Schema name (defaults to 'cc')
            
        Returns:
            List of table names
        """
        if self.table_cache is None:
            query = """
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = %s
                AND table_type = 'BASE TABLE'
                ORDER BY table_name;
            """
            self.cursor.execute(query, (schema,))
            self.table_cache = [row['table_name'] for row in self.cursor.fetchall()]
        return self.table_cache

    def get_column_info(self, table_name: str, schema: str = 'cc') -> List[Dict]:
        """
        Get column information for a specific table
        
        Args:
            table_name: Name of the table
            schema: Schema name (defaults to 'cc')
            
        Returns:
            List of column information dictionaries
        """
        cache_key = f"{schema}.{table_name}"
        if cache_key not in self.schema_cache:
            query = """
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_schema = %s
                AND table_name = %s
                ORDER BY ordinal_position;
            """
            self.cursor.execute(query, (schema, table_name))
            self.schema_cache[cache_key] = self.cursor.fetchall()
        return self.schema_cache[cache_key]

    def _extract_tables_from_query(self, query: str) -> List[str]:
        """Extract table names from a SQL query using regex"""
        # This is a simple implementation - might need to be enhanced for complex queries
        table_pattern = r'(?:FROM|JOIN)\s+(?:cc\.)?([a-zA-Z_][a-zA-Z0-9_]*)'
        return list(set(re.findall(table_pattern, query, re.IGNORECASE)))

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
            # First, get all available tables
            print("\nAvailable tables in schema:")
            tables = self.get_available_tables()
            for table in tables:
                print(f"- {table}")

            # Extract and show column information for tables in the query
            query_tables = self._extract_tables_from_query(query)
            for table in query_tables:
                print(f"\nColumns in table '{table}':")
                columns = self.get_column_info(table)
                for col in columns:
                    print(f"- {col['column_name']} ({col['data_type']})")

            print("\nExecuting query...")
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