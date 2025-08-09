# AWS Lambda Layer for DuckDB Python

A pre-built AWS Lambda Layer containing DuckDB for Python, making it easy to use DuckDB in your Lambda functions without worrying about package size limits or architecture.

## Overview

This project provides ready-to-use Lambda layers containing DuckDB Python bindings, optimized for AWS Lambda runtime environments.

### Features (Preview)

- 🚀 **Pre-built and optimized** for AWS Lambda Python 3.13 runtime
- 🌍 **Multi-region support** - Available in all AWS regions
- 🏗️ **Multiple architectures** - Support for both x86_64 and ARM64 (Graviton2)
- 📦 **Easy integration** - Just add the layer ARN to your Lambda function
- 🔄 **Automated builds** - Continuously updated with latest DuckDB versions
- 🆓 **Public layers** - No AWS account restrictions

## Quick Start

1. **Add the layer to your Lambda function:**

   ```bash
   # Using AWS CLI
   aws lambda update-function-configuration \
     --function-name your-function-name \
     --layers LAYER_ARN
   ```

2. **Use DuckDB in your Lambda function:**

   ```python
   import duckdb

   def lambda_handler(event, context):
       # Create an in-memory database
       conn = duckdb.connect(':memory:')

       # Execute a query
       result = conn.execute("SELECT 'Hello DuckDB!' as message").fetchall()

       return {
           'statusCode': 200,
           'body': result[0][0]
       }
   ```

## 🚧 Development Status

This project is currently under active development. The README will be updated soon with:

- ✅ Complete list of Layer ARNs for all regions
- ✅ Detailed usage examples and best practices
- ✅ Version compatibility matrix

**Stay tuned for updates!** ⭐ Star this repository to get notified when the full documentation is available.

## DuckDB layers

### Usage

- **x86_64**: `arn:aws:lambda:REGION:ACCOUNT_ID:layer:duckdb-python-x86_64:VERSION`
- **arm64**: `arn:aws:lambda:REGION:ACCOUNT_ID:layer:duckdb-python-arm64:VERSION`

To use the DuckDB layer in your Lambda function, add the appropriate layer ARN to your function configuration.

### Mappings

<!-- MAPPINGS-LIST:START -->
| Layer version | DuckDB version |
| ------------- | -------------- |
| 6 | v0.3.2 |
| 7 | v1.3.1 |
| 10 | v1.3.2 |
<!-- MAPPINGS-LIST:END -->

### Latest x86_64 layer ARNs

<!-- LATEST-x86_64:START -->
| Region | Layer ARN |
| ------ | --------- |
| us-east-1 | arn:aws:lambda:us-east-1:911510765542:layer:duckdb-python-x86_64:10 |
| us-east-2 | arn:aws:lambda:us-east-2:911510765542:layer:duckdb-python-x86_64:10 |
| us-west-1 | arn:aws:lambda:us-west-1:911510765542:layer:duckdb-python-x86_64:10 |
| us-west-2 | arn:aws:lambda:us-west-2:911510765542:layer:duckdb-python-x86_64:10 |
| af-south-1 | arn:aws:lambda:af-south-1:911510765542:layer:duckdb-python-x86_64:10 |
| ap-east-1 | arn:aws:lambda:ap-east-1:911510765542:layer:duckdb-python-x86_64:10 |
| ap-northeast-1 | arn:aws:lambda:ap-northeast-1:911510765542:layer:duckdb-python-x86_64:10 |
| ap-northeast-2 | arn:aws:lambda:ap-northeast-2:911510765542:layer:duckdb-python-x86_64:10 |
| ap-northeast-3 | arn:aws:lambda:ap-northeast-3:911510765542:layer:duckdb-python-x86_64:10 |
| ap-south-1 | arn:aws:lambda:ap-south-1:911510765542:layer:duckdb-python-x86_64:10 |
| ap-south-2 | arn:aws:lambda:ap-south-2:911510765542:layer:duckdb-python-x86_64:10 |
| ap-southeast-1 | arn:aws:lambda:ap-southeast-1:911510765542:layer:duckdb-python-x86_64:10 |
| ap-southeast-2 | arn:aws:lambda:ap-southeast-2:911510765542:layer:duckdb-python-x86_64:10 |
| ap-southeast-3 | arn:aws:lambda:ap-southeast-3:911510765542:layer:duckdb-python-x86_64:10 |
| ap-southeast-4 | arn:aws:lambda:ap-southeast-4:911510765542:layer:duckdb-python-x86_64:10 |
| ca-central-1 | arn:aws:lambda:ca-central-1:911510765542:layer:duckdb-python-x86_64:10 |
| eu-central-1 | arn:aws:lambda:eu-central-1:911510765542:layer:duckdb-python-x86_64:10 |
| eu-central-2 | arn:aws:lambda:eu-central-2:911510765542:layer:duckdb-python-x86_64:10 |
| eu-north-1 | arn:aws:lambda:eu-north-1:911510765542:layer:duckdb-python-x86_64:10 |
| eu-south-1 | arn:aws:lambda:eu-south-1:911510765542:layer:duckdb-python-x86_64:10 |
| eu-south-2 | arn:aws:lambda:eu-south-2:911510765542:layer:duckdb-python-x86_64:10 |
| eu-west-1 | arn:aws:lambda:eu-west-1:911510765542:layer:duckdb-python-x86_64:10 |
| eu-west-2 | arn:aws:lambda:eu-west-2:911510765542:layer:duckdb-python-x86_64:10 |
| eu-west-3 | arn:aws:lambda:eu-west-3:911510765542:layer:duckdb-python-x86_64:10 |
| il-central-1 | arn:aws:lambda:il-central-1:911510765542:layer:duckdb-python-x86_64:10 |
| me-central-1 | arn:aws:lambda:me-central-1:911510765542:layer:duckdb-python-x86_64:10 |
| me-south-1 | arn:aws:lambda:me-south-1:911510765542:layer:duckdb-python-x86_64:10 |
| sa-east-1 | arn:aws:lambda:sa-east-1:911510765542:layer:duckdb-python-x86_64:10 |
<!-- LATEST-x86_64:END -->

### Latest ARM64 layer ARNs

<!-- LATEST-arm64:START -->
| Region | Layer ARN |
| ------ | --------- |
| us-east-1 | arn:aws:lambda:us-east-1:911510765542:layer:duckdb-python-arm64:10 |
| us-east-2 | arn:aws:lambda:us-east-2:911510765542:layer:duckdb-python-arm64:10 |
| us-west-1 | arn:aws:lambda:us-west-1:911510765542:layer:duckdb-python-arm64:10 |
| us-west-2 | arn:aws:lambda:us-west-2:911510765542:layer:duckdb-python-arm64:10 |
| af-south-1 | arn:aws:lambda:af-south-1:911510765542:layer:duckdb-python-arm64:10 |
| ap-east-1 | arn:aws:lambda:ap-east-1:911510765542:layer:duckdb-python-arm64:10 |
| ap-northeast-1 | arn:aws:lambda:ap-northeast-1:911510765542:layer:duckdb-python-arm64:10 |
| ap-northeast-2 | arn:aws:lambda:ap-northeast-2:911510765542:layer:duckdb-python-arm64:10 |
| ap-northeast-3 | arn:aws:lambda:ap-northeast-3:911510765542:layer:duckdb-python-arm64:10 |
| ap-south-1 | arn:aws:lambda:ap-south-1:911510765542:layer:duckdb-python-arm64:10 |
| ap-south-2 | arn:aws:lambda:ap-south-2:911510765542:layer:duckdb-python-arm64:10 |
| ap-southeast-1 | arn:aws:lambda:ap-southeast-1:911510765542:layer:duckdb-python-arm64:10 |
| ap-southeast-2 | arn:aws:lambda:ap-southeast-2:911510765542:layer:duckdb-python-arm64:10 |
| ap-southeast-3 | arn:aws:lambda:ap-southeast-3:911510765542:layer:duckdb-python-arm64:10 |
| ap-southeast-4 | arn:aws:lambda:ap-southeast-4:911510765542:layer:duckdb-python-arm64:10 |
| ca-central-1 | arn:aws:lambda:ca-central-1:911510765542:layer:duckdb-python-arm64:10 |
| eu-central-1 | arn:aws:lambda:eu-central-1:911510765542:layer:duckdb-python-arm64:10 |
| eu-central-2 | arn:aws:lambda:eu-central-2:911510765542:layer:duckdb-python-arm64:10 |
| eu-north-1 | arn:aws:lambda:eu-north-1:911510765542:layer:duckdb-python-arm64:10 |
| eu-south-1 | arn:aws:lambda:eu-south-1:911510765542:layer:duckdb-python-arm64:10 |
| eu-south-2 | arn:aws:lambda:eu-south-2:911510765542:layer:duckdb-python-arm64:10 |
| eu-west-1 | arn:aws:lambda:eu-west-1:911510765542:layer:duckdb-python-arm64:10 |
| eu-west-2 | arn:aws:lambda:eu-west-2:911510765542:layer:duckdb-python-arm64:10 |
| eu-west-3 | arn:aws:lambda:eu-west-3:911510765542:layer:duckdb-python-arm64:10 |
| il-central-1 | arn:aws:lambda:il-central-1:911510765542:layer:duckdb-python-arm64:10 |
| me-central-1 | arn:aws:lambda:me-central-1:911510765542:layer:duckdb-python-arm64:10 |
| me-south-1 | arn:aws:lambda:me-south-1:911510765542:layer:duckdb-python-arm64:10 |
| sa-east-1 | arn:aws:lambda:sa-east-1:911510765542:layer:duckdb-python-arm64:10 |
<!-- LATEST-arm64:END -->

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
