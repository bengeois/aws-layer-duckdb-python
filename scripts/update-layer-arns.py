#!/usr/bin/env python3

import json
import os
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--duckdb-version", required=True)
    parser.add_argument("--layer-version", required=True)
    parser.add_argument("--python-versions", required=True)
    parser.add_argument("--account-id", required=True)
    parser.add_argument("--aws-regions", required=True)
    args = parser.parse_args()

    regions = args.aws_regions.split(",")
    python_versions = args.python_versions.split(",")
    
    arns_file = Path(__file__).parent.parent / "data" / "arns.json"
    
    # Charge ou initialise les données
    arns_data = {}
    if arns_file.exists():
        with open(arns_file, 'r') as f:
            arns_data = json.load(f)
    
    # Initialise la structure
    if args.duckdb_version not in arns_data:
        arns_data[args.duckdb_version] = {}
    
    # Génère les ARNs
    for python_version in python_versions:
        if python_version not in arns_data[args.duckdb_version]:
            arns_data[args.duckdb_version][python_version] = {}
        
        for architecture in ["x86_64", "arm64"]:
            if architecture not in arns_data[args.duckdb_version][python_version]:
                arns_data[args.duckdb_version][python_version][architecture] = {}
            
            python_formatted = python_version.replace('.', '')
            layer_name = f"duckdb-python{python_formatted}-{architecture}"
            
            for region in regions:
                arn = f"arn:aws:lambda:{region}:{args.account_id}:layer:{layer_name}:{args.layer_version}"
                arns_data[args.duckdb_version][python_version][architecture][region] = arn
    
    # Sauvegarde
    with open(arns_file, 'w') as f:
        json.dump(arns_data, f, indent=4, sort_keys=True)


if __name__ == "__main__":
    main()