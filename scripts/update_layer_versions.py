#!/usr/bin/env python3
"""
Script to update layer-versions.json with new DuckDB and layer version information.
"""
import json
import sys
import os
from datetime import datetime

def update_layer_versions(duckdb_version, layer_version, json_file_path):
    """
    Update the layer-versions.json file with new version information.
    
    Args:
        duckdb_version (str): The DuckDB version (e.g., "1.3.2")
        layer_version (str): The AWS Lambda layer version (e.g., "42")
        json_file_path (str): Path to the layer-versions.json file
    """
    # Load existing data or create new structure
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as f:
            data = json.load(f)
    else:
        data = {}
    
    # Add or update the version entry
    data[duckdb_version] = {
        "layer_version": layer_version,
        "updated_at": datetime.utcnow().isoformat() + "Z"
    }
    
    # Write back to file with nice formatting
    with open(json_file_path, 'w') as f:
        json.dump(data, f, indent=2, sort_keys=True)
    
    print(f"Updated layer-versions.json: DuckDB {duckdb_version} -> Layer version {layer_version}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python update_layer_versions.py <duckdb_version> <layer_version>")
        print("Example: python update_layer_versions.py 1.3.2 42")
        sys.exit(1)
    
    duckdb_version = sys.argv[1]
    layer_version = sys.argv[2]
    
    # Path to the JSON file (relative to script location)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(script_dir, '..', 'layer-versions.json')
    
    update_layer_versions(duckdb_version, layer_version, json_file_path)

if __name__ == "__main__":
    main()
