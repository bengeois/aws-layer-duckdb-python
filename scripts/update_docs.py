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
    if len(sys.argv) != 3:
        print("Incorrect number of arguments for update_docs.py")
        sys.exit(1)
    
    duckdb_version = sys.argv[1]
    layer_version = sys.argv[2]

    print(f"Updating documentation for DuckDB {duckdb_version} with layer version {layer_version}")
    
    # Step 1: Update mappings (which also updates layer-versions.json)
    print("Step 1: Updating layer-versions.json and mappings table in README.md...")
    if not run_script("update_mappings.py", [duckdb_version, layer_version]):
        print("Step 1: Failed to update layer-versions.json")
        sys.exit(1)
    
    # Step 2: Update ARN tables
    print("Step 2: Updating ARN tables in README.md...")
    if not run_script("update_arns.py"):
        print("Step 2: Failed to update ARN tables")
        sys.exit(1)

    print("Documentation updates completed successfully!")

if __name__ == "__main__":
    main()
