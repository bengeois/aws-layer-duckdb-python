ARG ARCHITECTURE=amd64
ARG PYTHON_VERSION=3.13
FROM --platform=linux/${ARCHITECTURE} python:${PYTHON_VERSION}-slim

ARG DUCKDB_VERSION

WORKDIR /tmp

# Detect the package manager and install zip
RUN apt-get update && apt-get install -y \
    zip

# Install DuckDB package
RUN pip install duckdb==${DUCKDB_VERSION} --no-cache-dir -t /tmp/python

# Prepare the zip file for Lambda Layer
RUN zip -r duckdb.zip python