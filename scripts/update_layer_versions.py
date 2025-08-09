#!/usr/bin/env python3
"""
Script to update layer-versions.json with new DuckDB and layer version information.
Also updates the mappings table and ARN tables in README.md.
"""
import json
import sys
import os
import re
from datetime import datetime

# AWS regions list (same as in the workflow)
AWS_REGIONS = [
    "us-east-1", "us-east-2", "us-west-1", "us-west-2",
    "af-south-1", "ap-east-1", "ap-northeast-1", "ap-northeast-2", 
    "ap-northeast-3", "ap-south-1", "ap-south-2", "ap-southeast-1",
    "ap-southeast-2", "ap-southeast-3", "ap-southeast-4", "ca-central-1",
    "eu-central-1", "eu-central-2", "eu-north-1", "eu-south-1",
    "eu-south-2", "eu-west-1", "eu-west-2", "eu-west-3",
    "il-central-1", "me-central-1", "me-south-1", "sa-east-1"
]

# AWS Account ID (extracted from the workflow)
AWS_ACCOUNT_ID = "911510765542"

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

def get_latest_layer_version(data):
    """Get the latest layer version from the data."""
    if not data:
        raise ValueError("No layer versions found in data")
    
    # Sort by layer version and get the latest
    sorted_items = sorted(data.items(), key=lambda x: int(x[1]['layer_version']))
    latest_version = sorted_items[-1][1]['layer_version']
    return latest_version

def update_content_between_delimiters(content, start_delimiter, end_delimiter, new_content):
    """Update content between two delimiters."""
    if start_delimiter not in content or end_delimiter not in content:
        raise ValueError(f"Could not find delimiters '{start_delimiter}' and/or '{end_delimiter}' in README.md")
    
    start_pos = content.find(start_delimiter)
    end_pos = content.find(end_delimiter)
    
    if start_pos == -1 or end_pos == -1:
        raise ValueError("Could not locate delimiter positions in README.md")
    
    # Calculate positions after start delimiter and before end delimiter
    start_replace = start_pos + len(start_delimiter)
    end_replace = end_pos
    
    # Replace the content between delimiters
    return content[:start_replace] + new_content + content[end_replace:]

def update_readme_mappings(data, readme_path):
    """Update the mappings table in README.md between delimiters."""
    if not os.path.exists(readme_path):
        raise FileNotFoundError(f"README.md not found at {readme_path}")
    
    with open(readme_path, 'r') as f:
        content = f.read()
    
    # Generate the mappings table
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
    
    table_lines.append("")  # Empty line before end delimiter
    new_table = '\n'.join(table_lines)
    
    # Update mappings table
    content = update_content_between_delimiters(
        content, 
        "<!-- MAPPINGS-LIST:START -->", 
        "<!-- MAPPINGS-LIST:END -->", 
        new_table
    )
    
    print(f"Updated README.md mappings table with {len(sorted_items)} entries")
    return content

def update_readme_arn_tables(data, content):
    """Update both x86_64 and arm64 ARN tables in README.md."""
    latest_layer_version = get_latest_layer_version(data)
    
    # Update x86_64 ARN table
    x86_table_lines = [
        "",  # Empty line after start delimiter
        "| Region | Layer ARN |",
        "| ------ | --------- |"
    ]
    
    for region in AWS_REGIONS:
        arn = f"arn:aws:lambda:{region}:{AWS_ACCOUNT_ID}:layer:duckdb-python-x86_64:{latest_layer_version}"
        x86_table_lines.append(f"| {region} | {arn} |")
    
    x86_table_lines.append("")  # Empty line before end delimiter
    x86_table = '\n'.join(x86_table_lines)
    
    # Update x86_64 table
    content = update_content_between_delimiters(
        content,
        "<!-- LATEST-x86_64:START -->",
        "<!-- LATEST-x86_64:END -->",
        x86_table
    )
    
    # Update arm64 ARN table
    arm64_table_lines = [
        "",  # Empty line after start delimiter
        "| Region | Layer ARN |",
        "| ------ | --------- |"
    ]
    
    for region in AWS_REGIONS:
        arn = f"arn:aws:lambda:{region}:{AWS_ACCOUNT_ID}:layer:duckdb-python-arm64:{latest_layer_version}"
        arm64_table_lines.append(f"| {region} | {arn} |")
    
    arm64_table_lines.append("")  # Empty line before end delimiter
    arm64_table = '\n'.join(arm64_table_lines)
    
    # Update arm64 table
    content = update_content_between_delimiters(
        content,
        "<!-- LATEST-arm64:START -->",
        "<!-- LATEST-arm64:END -->",
        arm64_table
    )
    
    print(f"Updated README.md ARN tables for both architectures with layer version {latest_layer_version}")
    return content

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
    content = update_readme_mappings(data, readme_path)
    
    # Update README ARN tables
    content = update_readme_arn_tables(data, content)
    
    # Write the final content back to README
    with open(readme_path, 'w') as f:
        f.write(content)
    
    print("All updates completed successfully!")

if __name__ == "__main__":
    main()
