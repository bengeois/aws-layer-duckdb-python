#!/usr/bin/env python3
"""
This script coordinates the execution of update_mappings.py and update_arns.py.
"""
import sys
import os
import subprocess

def run_script(script_name, args=None):
    """Run a Python script with optional arguments."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, script_name)
    
    cmd = [sys.executable, script_path]
    if args:
        cmd.extend(args)
    
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}:")
        print(e.stderr)
        return False

def main():
    if len(sys.argv) != 6:
        print("Usage: update-docs.py <aws_account_id> <duckdb_version> <layer_version> <aws_regions> <python_versions>")
        sys.exit(1)

    aws_account_id = sys.argv[1]
    duckdb_version = sys.argv[2]
    layer_version = sys.argv[3]
    aws_regions = sys.argv[4]
    python_versions = sys.argv[5]

    print(f"Updating documentation for DuckDB {duckdb_version} with layer version {layer_version} and Python versions {python_versions}")

    print("Step 1: Updating arns.json file...")
    if not run_script("update-layer-arns.py", [
        "--account-id", aws_account_id,
        "--duckdb-version", duckdb_version,
        "--layer-version", layer_version,
        "--aws-regions", aws_regions,
        "--python-versions", python_versions
    ]):
        print("Step 1: Failed to update arns.json")
        sys.exit(1)

    print("Step 2: Updating layer mappings...")
    if not run_script("update-mappings.py", [duckdb_version, layer_version]):
        print("Step 2: Failed to update layer mappings")
        sys.exit(1)

    print("Documentation updates completed successfully!")

if __name__ == "__main__":
    main()
