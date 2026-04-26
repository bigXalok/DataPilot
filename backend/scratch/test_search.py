import os
import sys

# Add the backend directory to sys.path
backend_dir = "/Users/alokkumar/Desktop/DataPilot/backend"
sys.path.append(backend_dir)

from app.vector_store import search_vector_store

try:
    # Search for something that might be in a RIL report
    query = "What is the net profit of Reliance?"
    results = search_vector_store(query)
    print(f"Search Results:\n{results[:500]}...")
except Exception as e:
    print(f"Error: {str(e)}")
