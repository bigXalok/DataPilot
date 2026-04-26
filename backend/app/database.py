import pandas as pd
from sqlalchemy import create_engine, inspect
import os

DB_URL = "sqlite:///./datapilot.db"
engine = create_engine(DB_URL)

def csv_to_sql(file_path: str, table_name: str):
    """
    Reads a CSV file and saves it as a table in the SQLite database.
    """
    df = pd.read_csv(file_path)
    # Clean column names (replace spaces and special characters)
    df.columns = [c.lower().replace(' ', '_').replace('(', '').replace(')', '') for c in df.columns]
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    return table_name

def get_db_schema():
    """
    Returns the schema of the database for the LLM to understand.
    """
    inspector = inspect(engine)
    schema_info = ""
    for table_name in inspector.get_table_names():
        schema_info += f"Table: {table_name}\n"
        columns = inspector.get_columns(table_name)
        for column in columns:
            schema_info += f"  - {column['name']} ({column['type']})\n"
        schema_info += "\n"
    return schema_info

def run_query(query: str):
    """
    Executes a SQL query and returns the results as a list of dictionaries.
    """
    with engine.connect() as conn:
        result = conn.execute(query)
        return [dict(row) for row in result.mappings()]
