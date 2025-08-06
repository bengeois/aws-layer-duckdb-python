ARG LAMBDA_ARCHITECTURE

FROM amazon/aws-lambda-python:3.13-${LAMBDA_ARCHITECTURE}

ARG DUCKDB_VERSION

WORKDIR /tmp

# Update and install necessary packages
RUN dnf update -y && dnf install -y zip 

# Create a directory for DuckDB and install the package
RUN mkdir -p /tmp/duckdb && \
    pip install duckdb==${DUCKDB_VERSION} --no-cache-dir -t /tmp/duckdb

# Prepare the zip file for Lambda Layer
RUN mkdir -p /tmp/python && \
    cp -r /tmp/duckdb/* /tmp/python/ && \
    zip -r duckdb.zip python