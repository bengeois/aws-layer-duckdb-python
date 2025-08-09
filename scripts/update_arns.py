#!/usr/bin/env python3
"""
Script to update ARN tables in README.md for both x86_64 and arm64 architectures.
"""
import json
import sys
import os

def get_latest_layer_version(json_file_path):
    """Get the latest layer version from the layer-versions.json file."""
    if not os.path.exists(json_file_path):
        raise FileNotFoundError(f"layer-versions.json not found at {json_file_path}")
    
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    if not data:
        raise ValueError("No layer versions found in data")
    
    # Sort by layer version and get the latest
    sorted_items = sorted(data.items(), key=lambda x: int(x[1]['layer_version']))
    latest_version = sorted_items[-1][1]['layer_version']
    return latest_version

def parse_regions_from_env():
    """Parse AWS regions from environment variable."""
    regions_env = os.getenv('AWS_REGIONS', '')
    if not regions_env:
        raise ValueError("AWS_REGIONS environment variable is not set")
    
    # Split by comma and clean up whitespace
    regions = [region.strip() for region in regions_env.split(',') if region.strip()]
    if not regions:
        raise ValueError("AWS_REGIONS environment variable is empty or invalid")
    
    return regions

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

def update_readme_arn_tables(readme_path, json_file_path):
    """Update both x86_64 and arm64 ARN tables in README.md."""
    if not os.path.exists(readme_path):
        raise FileNotFoundError(f"README.md not found at {readme_path}")
    
    # Get configuration from environment
    aws_regions = parse_regions_from_env()
    aws_account_id = os.getenv('AWS_ACCOUNT_ID')
    latest_layer_version = get_latest_layer_version(json_file_path)
    
    with open(readme_path, 'r') as f:
        content = f.read()
    
    # Update x86_64 ARN table
    x86_table_lines = [
        "",  # Empty line after start delimiter
        "| Region | Layer ARN |",
        "| ------ | --------- |"
    ]
    
    for region in aws_regions:
        arn = f"arn:aws:lambda:{region}:{aws_account_id}:layer:duckdb-python-x86_64:{latest_layer_version}"
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
    
    for region in aws_regions:
        arn = f"arn:aws:lambda:{region}:{aws_account_id}:layer:duckdb-python-arm64:{latest_layer_version}"
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
    
    # Write the final content back to README
    with open(readme_path, 'w') as f:
        f.write(content)
    
    print(f"Updated README.md ARN tables for both architectures with layer version {latest_layer_version}")
    print(f"Updated {len(aws_regions)} regions with Account ID: {aws_account_id}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(script_dir, '..', 'layer-versions.json')
    readme_path = os.path.join(script_dir, '..', 'README.md')
    
    update_readme_arn_tables(readme_path, json_file_path)

if __name__ == "__main__":
    main()
