from sqlalchemy import text
import sys
import os

# Add the backend directory to sys.path
backend_dir = "/Users/alokkumar/Desktop/DataPilot/backend"
sys.path.append(backend_dir)

from app.database import engine

with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS test_json"))
    conn.commit()
    print("Table 'test_json' dropped.")
