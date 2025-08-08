ARG ARCHITECTURE

FROM amazon/aws-lambda-python:3.13-${ARCHITECTURE}

ARG DUCKDB_VERSION

WORKDIR /tmp

# Detect the package manager and install zip
RUN if command -v dnf &> /dev/null; then \
        dnf update -y && dnf install -y zip; \
    elif command -v yum &> /dev/null; then \
        yum update -y && yum install -y zip; \
    elif command -v apk &> /dev/null; then \
        apk update && apk add zip; \
    else \
        echo "Unsupported package manager" && exit 1; \
    fi

# Install DuckDB package
RUN pip install duckdb==${DUCKDB_VERSION} --no-cache-dir -t /tmp/python

# Prepare the zip file for Lambda Layer
RUN zip -r duckdb.zip python
