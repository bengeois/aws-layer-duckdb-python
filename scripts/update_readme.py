#!/usr/bin/env python3
import json
import os
from pathlib import Path

START_DELIM = "<!-- COMPATIBILITY-LIST:START -->"
END_DELIM = "<!-- COMPATIBILITY-LIST:END -->"

def update_content_between_delimiters(content, start_delimiter, end_delimiter, new_content):
    """Replace content between delimiters with new_content."""
    if start_delimiter not in content or end_delimiter not in content:
        raise ValueError(f"Delimiters {start_delimiter} / {end_delimiter} not found in README.md")

    start_pos = content.find(start_delimiter) + len(start_delimiter)
    end_pos = content.find(end_delimiter)

    return content[:start_pos] + "\n" + new_content + "\n" + content[end_pos:]


def build_table(arns_data):
    """Build Markdown table from arns.json."""
    lines = [
        "",
        "| DuckDB version | Python versions | Architectures |",
        "| -------------- | --------------- | ------------- |"
    ]

    for duckdb_ver, py_map in sorted(arns_data.items()):
        python_versions = sorted(py_map.keys())
        architectures = sorted(
            {arch for archs in py_map.values() for arch in archs.keys()}
        )

        lines.append(
            f"| {duckdb_ver} | {', '.join(python_versions)} | {', '.join(architectures)} |"
        )

    lines.append("")
    return "\n".join(lines)


def main():
    repo_root = Path(__file__).parent.parent
    readme_path = repo_root / "README.md"
    arns_path = repo_root / "data" / "arns.json"

    if not arns_path.exists():
        raise FileNotFoundError("data/arns.json not found")

    with open(arns_path) as f:
        arns_data = json.load(f)

    new_table = build_table(arns_data)

    with open(readme_path) as f:
        content = f.read()

    updated = update_content_between_delimiters(content, START_DELIM, END_DELIM, new_table)

    with open(readme_path, "w") as f:
        f.write(updated)

    print("✅ README.md updated with DuckDB mappings table.")


if __name__ == "__main__":
    main()
