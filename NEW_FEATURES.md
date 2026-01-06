# 🚀 PipeX v2.0 - New Features & Enhancements

## 📁 Enhanced File Organization

### Automatic Directory Creation

- Output files are now automatically organized in structured directories
- Timestamp support for unique file naming
- Configurable directory structures

```yaml
load:
  target: "Local File"
  config:
    file_type: "csv"
    file_path: "output/processed/data.csv"
    add_timestamp: true # Creates: data_20240106_143022.csv
```

## 🔄 Advanced Transformation System

### Multiple Script Support

Execute multiple transformation scripts in sequence:

```yaml
transform:
  scripts:
    - "transforms/step1_cleaning.py"
    - "transforms/step2_enrichment.py"
    - "transforms/step3_validation.py"
  config:
    fail_on_script_error: false # Continue if one script fails
```

### Default Transformation Library

Built-in transformations for common use cases:

```yaml
transform:
  config:
    use_default_transforms: true
    default_config:
      clean_data: true
      feature_engineering: true
      add_metadata: true
      validate_data: true
```

### Industry-Specific Transformations

Pre-built transformations for different industries:

```python
# In your transform script
def transform(data, config):
    from app.default_transforms import industry_specific_transform
    return industry_specific_transform(data, 'finance', config)
```

## 📊 Multi-Format File Support

### Enhanced File Types

- **Excel**: `.xlsx`, `.xls` with sheet selection
- **Parquet**: High-performance columnar format
- **XML**: Structured data extraction
- **JSON**: Multiple orientations and line formats

```yaml
extract:
  source: "file"
  connection_details:
    file_type: "excel"
    sheet_name: "Sheet1"
    skiprows: 2
    nrows: 1000
  query_or_endpoint: "data/input.xlsx"
```

### Advanced CSV Options

```yaml
extract:
  source: "file"
  connection_details:
    file_type: "csv"
    separator: ";"
    encoding: "utf-8"
    skiprows: 1
    nrows: 10000
```

## ☁️ Multi-Cloud Storage Support

### AWS S3

```yaml
load:
  target: "Cloud Storage"
  config:
    provider: "aws"
    bucket_name: "${AWS_BUCKET_NAME}"
    file_name: "data.csv"
    format: "csv"
```

### Google Cloud Storage

```yaml
load:
  target: "Cloud Storage"
  config:
    provider: "gcp"
    bucket_name: "${GCP_BUCKET_NAME}"
    file_name: "data.parquet"
    format: "parquet"
    project_id: "${GOOGLE_CLOUD_PROJECT}"
```

### Azure Blob Storage

```yaml
load:
  target: "Cloud Storage"
  config:
    provider: "azure"
    bucket_name: "${AZURE_CONTAINER_NAME}"
    file_name: "data.json"
    format: "json"
    connection_string: "${AZURE_STORAGE_CONNECTION_STRING}"
```

### DigitalOcean Spaces

```yaml
load:
  target: "Cloud Storage"
  config:
    provider: "digitalocean"
    bucket_name: "${DO_SPACES_BUCKET}"
    file_name: "data.csv"
    access_key_id: "${DO_SPACES_ACCESS_KEY_ID}"
    secret_access_key: "${DO_SPACES_SECRET_ACCESS_KEY}"
```

## 🚨 Intelligent Error Handling

### User-Friendly Error Messages

Errors now include:

- **Clear problem description**
- **Actionable solutions**
- **Context information**
- **Technical details**

### Example Error Output

```
❌ Configuration Error: Required configuration keys are missing

📋 Context:
  • config_file: config.yaml
  • missing_keys: ['extract.source']

💡 Suggested Solutions:
  1. Check your configuration file: config.yaml
  2. Ensure all required sections (extract, transform, load) are present
  3. Validate your configuration with: pipex validate config.yaml
  4. Refer to the documentation for configuration examples

🔍 Technical Details: KeyError: 'source'
```

### Error Categories

- **Configuration**: YAML syntax, missing keys, environment variables
- **Authentication**: Cloud credentials, API keys, permissions
- **Network**: Timeouts, connection failures, SSL issues
- **File System**: Missing files, permissions, disk space
- **Data Format**: JSON parsing, CSV delimiters, encoding
- **Dependencies**: Missing packages, version conflicts

## 🔧 Installation Options

### Core Installation

```bash
pip install pipex
```

### With Cloud Support

```bash
pip install pipex[aws]        # AWS S3 support
pip install pipex[gcp]        # Google Cloud Storage
pip install pipex[azure]      # Azure Blob Storage
pip install pipex[all]        # All cloud providers
```

### With File Format Support

```bash
pip install pipex[excel]      # Excel file support
pip install pipex[parquet]    # Parquet format support
pip install pipex[xml]        # XML parsing support
```

## 📋 Environment Variables

### Multi-Cloud Credentials

```bash
# AWS
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_REGION=us-east-1

# Google Cloud
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
GOOGLE_CLOUD_PROJECT=your-project-id

# Azure
AZURE_STORAGE_CONNECTION_STRING=your-connection-string
# OR
AZURE_STORAGE_ACCOUNT_NAME=your-account
AZURE_STORAGE_ACCOUNT_KEY=your-key

# DigitalOcean Spaces
DO_SPACES_ACCESS_KEY_ID=your-key
DO_SPACES_SECRET_ACCESS_KEY=your-secret
DO_SPACES_REGION=nyc3
```

## 🎯 Usage Examples

### Multi-Format Pipeline

```bash
# Extract from Excel, transform, load to Parquet in GCS
pipex run --config examples/excel_to_gcs_parquet.yaml

# Process multiple CSV files to Azure
pipex run --config examples/csv_batch_to_azure.yaml

# API to multi-cloud with transformations
pipex run --config examples/api_to_multicloud.yaml
```

### Advanced Transformations

```bash
# Use multiple transformation scripts
pipex transform scripts/clean.py,scripts/enrich.py config.yaml data.csv

# Industry-specific transformations
pipex run --config examples/finance_pipeline.yaml

# Default transformations only
pipex run --config examples/default_transforms.yaml
```

### Error Diagnosis

```bash
# Validate configuration
pipex validate config.yaml

# Dry run to check for issues
pipex run --config config.yaml --dry-run

# Verbose logging for debugging
pipex run --config config.yaml --verbose
```

## 🔄 Migration from v1.0

### Configuration Updates

1. **Cloud Storage**: Update `target: "S3 Bucket"` to `target: "Cloud Storage"` and add `provider`
2. **Transform Scripts**: Change single `script` to `scripts` array for multiple scripts
3. **File Paths**: Add directory structure to `file_path` configurations

### New Optional Dependencies

```bash
# Install additional packages as needed
pip install openpyxl          # Excel support
pip install google-cloud-storage  # GCS support
pip install azure-storage-blob    # Azure support
pip install pyarrow          # Parquet support
```

## 📈 Performance Improvements

### Optimized File Processing

- **Chunked reading** for large files
- **Memory-efficient** transformations
- **Parallel processing** for multiple scripts
- **Caching** for repeated operations

### Cloud Storage Optimization

- **Streaming uploads** for large datasets
- **Compression** support for all formats
- **Retry logic** with exponential backoff
- **Connection pooling** for multiple operations

## 🛡️ Security Enhancements

### Credential Management

- **Environment variable** priority over config files
- **Secure credential** storage recommendations
- **Permission validation** before operations
- **Audit logging** for all operations

### Data Protection

- **Encryption in transit** for all cloud operations
- **Temporary file cleanup** after processing
- **Sensitive data masking** in logs
- **Access control** validation

## 🔮 Coming Soon

### Planned Features

- **Real-time streaming** data processing
- **Kubernetes operator** for scalable deployments
- **Web UI** for pipeline management
- **Data lineage** tracking and visualization
- **Advanced scheduling** with cron expressions
- **Data quality** monitoring and alerting

### Community Contributions

- **Plugin system** for custom data sources
- **Transformation marketplace** for sharing scripts
- **Integration templates** for popular services
- **Performance benchmarking** tools
