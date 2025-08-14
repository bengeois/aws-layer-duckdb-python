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

- **x86_64**: `arn:aws:lambda:${REGION}:${ACCOUNT_ID}:layer:duckdb-python${PYTHON_VERSION}-x86_64:${LAYER_VERSION}`
- **arm64**: `arn:aws:lambda:${REGION}:${ACCOUNT_ID}:layer:duckdb-python${PYTHON_VERSION}-arm64:${LAYER_VERSION}`

To use the DuckDB layer in your Lambda function, add the appropriate layer ARN to your function configuration.

### Mappings

<!-- MAPPINGS-LIST:START -->
| Layer version | DuckDB version |
| ------------- | -------------- |
| 2 | v0.9.0 |
<!-- MAPPINGS-LIST:END -->

You can find the complete list of layer ARNs in the [data/arns.json](data/arns.json) file.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
