ARG LAMBDA_ARCHITECTURE

FROM amazon/aws-lambda-python:3.13-${LAMBDA_ARCHITECTURE}

ARG DUCKDB_VERSION

WORKDIR /tmp

# Update and install necessary packages
RUN dnf update -y && dnf install -y zip

# Install DuckDB package
RUN pip install duckdb==${DUCKDB_VERSION} --no-cache-dir -t /tmp/python

# Prepare the zip file for Lambda Layer
RUN zip -r duckdb.zip python
