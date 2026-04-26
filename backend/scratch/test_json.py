import os
import sys
import json

# Add the backend directory to sys.path
backend_dir = "/Users/alokkumar/Desktop/DataPilot/backend"
sys.path.append(backend_dir)

from app.database import file_to_sql

# Create a small test JSON file
test_file = os.path.join(backend_dir, "uploads", "test.json")
data = [{"name": "Product A", "sales": 100}, {"name": "Product B", "sales": 200}]
with open(test_file, "w") as f:
    json.dump(data, f)

try:
    table_name = file_to_sql(test_file, "test_json")
    print(f"Success! Processed into table '{table_name}'.")
except Exception as e:
    print(f"Error: {str(e)}")
finally:
    if os.path.exists(test_file):
        os.remove(test_file)
