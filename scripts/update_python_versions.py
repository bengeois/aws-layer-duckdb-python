#!/usr/bin/env python3
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

repo_root = Path(__file__).parent.parent


def fetch_duckdb_pythons(version: str) -> set[str]:
    url = f"https://pypi.org/pypi/duckdb/{version}/json"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.load(response)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Error: DuckDB {version} not found on PyPI.", file=sys.stderr)
        else:
            print(
                f"Error: PyPI returned HTTP {e.code} for DuckDB {version}.",
                file=sys.stderr,
            )
        sys.exit(1)
    pythons = set()
    for file in data["urls"]:
        filename = file["filename"]
        if "manylinux" not in filename:
            continue
        match = re.search(r"cp3(\d+)", filename)
        if match:
            pythons.add(f"3.{match.group(1)}")
    return pythons


def read_lambda_runtimes() -> set[str]:
    path = repo_root / ".github" / ".lambda-python-runtimes"
    return {line.strip() for line in path.read_text().splitlines() if line.strip()}


def read_python_versions() -> set[str]:
    path = repo_root / ".github" / "workflows" / "build-layer.yml"
    match = re.search(r'PYTHON_VERSIONS:\s*"([^"]+)"', path.read_text())
    if not match:
        print("Error: PYTHON_VERSIONS not found in build-layer.yml", file=sys.stderr)
        sys.exit(1)
    return {v.strip() for v in match.group(1).split(",")}


def write_python_versions(versions: set[str]) -> None:
    def ver_key(v: str) -> tuple:
        return tuple(int(x) for x in v.split("."))

    formatted = ",".join(sorted(versions, key=ver_key))
    path = repo_root / ".github" / "workflows" / "build-layer.yml"
    content = path.read_text()
    updated = re.sub(r'(PYTHON_VERSIONS:\s*")[^"]+(")', rf"\g<1>{formatted}\2", content)
    path.write_text(updated)


def main():
    duckdb_version = (repo_root / ".github" / ".duckdb-version").read_text().strip()

    duckdb_pythons = fetch_duckdb_pythons(duckdb_version)
    lambda_runtimes = read_lambda_runtimes()
    current = read_python_versions()
    expected = duckdb_pythons & lambda_runtimes

    if expected == current:
        print(f"PYTHON_VERSIONS already up to date for DuckDB {duckdb_version}.")
        return

    def ver_key(v: str) -> tuple:
        return tuple(int(x) for x in v.split("."))

    write_python_versions(expected)
    print(f"PYTHON_VERSIONS updated for DuckDB {duckdb_version}:")
    for v in sorted(expected - current, key=ver_key):
        print(f"  + {v}")
    for v in sorted(current - expected, key=ver_key):
        print(f"  - {v}")


if __name__ == "__main__":
    main()
