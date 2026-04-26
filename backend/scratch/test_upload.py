import os
import sys

# Add the backend directory to sys.path
backend_dir = "/Users/alokkumar/Desktop/DataPilot/backend"
sys.path.append(backend_dir)

from app.vector_store import process_file

# Create a small test file
test_file = os.path.join(backend_dir, "uploads", "test.txt")
with open(test_file, "w") as f:
    f.write("This is a test file for DataPilot vector store.")

try:
    num_chunks = process_file(test_file)
    print(f"Success! Processed into {num_chunks} chunks.")
except Exception as e:
    print(f"Error: {str(e)}")
finally:
    if os.path.exists(test_file):
        os.remove(test_file)
