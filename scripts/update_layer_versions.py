#!/usr/bin/env python3
"""
Script to update layer-versions.json with new DuckDB and layer version information.
Also updates the mappings table in README.md.
"""
import json
import sys
import os
import re
from datetime import datetime

def update_layer_versions(duckdb_version, layer_version, json_file_path):
    """
    Update the layer-versions.json file with new version information.
    
    Args:
        duckdb_version (str): The DuckDB version (e.g., "1.3.2")
        layer_version (str): The AWS Lambda layer version (e.g., "42")
        json_file_path (str): Path to the layer-versions.json file
    """
    # Load the layer versions file
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as f:
            data = json.load(f)
    else:
        data = {}
    
    data[duckdb_version] = {
        "layer_version": layer_version,
        "updated_at": datetime.utcnow().isoformat() + "Z"
    }
    
    with open(json_file_path, 'w') as f:
        json.dump(data, f, indent=2, sort_keys=True)
    
    print(f"Updated layer-versions.json: DuckDB {duckdb_version} -> Layer version {layer_version}")
    return data

def update_readme_mappings(data, readme_path):
    """
    Update the mappings table in README.md between delimiters.
    
    Args:
        data (dict): The layer versions data
        readme_path (str): Path to the README.md file
    """
    if not os.path.exists(readme_path):
        raise FileNotFoundError(f"README.md not found at {readme_path}")
    
    with open(readme_path, 'r') as f:
        content = f.read()
    
    # Check if delimiters exist
    start_delimiter = "<!-- MAPPINGS-LIST:START -->"
    end_delimiter = "<!-- MAPPINGS-LIST:END -->"
    
    if start_delimiter not in content or end_delimiter not in content:
        raise ValueError(f"Could not find delimiters '{start_delimiter}' and/or '{end_delimiter}' in README.md")
    
    table_lines = [
        "",  # Empty line after start delimiter
        "| Layer version | DuckDB version |",
        "| ------------- | -------------- |"
    ]
    
    # Sort by layer version
    sorted_items = sorted(data.items(), key=lambda x: int(x[1]['layer_version']))
    
    for duckdb_ver, info in sorted_items:
        layer_ver = info['layer_version']
        display_version = duckdb_ver if duckdb_ver.startswith('v') else f'v{duckdb_ver}'
        table_lines.append(f"| {layer_ver} | {display_version} |")
    
    # Empty line before end delimiter
    table_lines.append("")
    
    new_table = '\n'.join(table_lines)
    
    # Find and replace content between delimiters
    start_pos = content.find(start_delimiter)
    end_pos = content.find(end_delimiter)
    
    if start_pos == -1 or end_pos == -1:
        raise ValueError("Could not locate delimiter positions in README.md")
    
    # Calculate positions after start delimiter and before end delimiter
    start_replace = start_pos + len(start_delimiter)
    end_replace = end_pos
    
    # Replace the content between delimiters
    new_content = content[:start_replace] + new_table + content[end_replace:]
    
    with open(readme_path, 'w') as f:
        f.write(new_content)
    
    print(f"Updated README.md mappings table with {len(sorted_items)} entries")

def main():
    if len(sys.argv) != 3:
        print("Usage: python update_layer_versions.py <duckdb_version> <layer_version>")
        print("Example: python update_layer_versions.py 1.3.2 42")
        sys.exit(1)
    
    duckdb_version = sys.argv[1]
    layer_version = sys.argv[2]
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(script_dir, '..', 'layer-versions.json')
    readme_path = os.path.join(script_dir, '..', 'README.md')
    
    # Update JSON file
    data = update_layer_versions(duckdb_version, layer_version, json_file_path)
    
    # Update README mappings table
    update_readme_mappings(data, readme_path)

if __name__ == "__main__":
    main()
