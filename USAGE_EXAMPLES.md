# PipeX Usage Examples

This document provides comprehensive examples of how to use PipeX for various ETL scenarios.

## 🚀 Quick Start Examples

### 1. Basic API to File Pipeline

```bash
# Run complete pipeline
pipex run --config config.yaml

# With dry-run validation
pipex run --config config.yaml --dry-run

# With verbose logging
pipex run --config config.yaml --verbose
```

### 2. Individual Stage Commands

```bash
# Extract data from API
pipex extract api config.yaml --output raw_data.csv

# Transform data with custom script
pipex transform transform_script.py config.yaml raw_data.csv --output clean_data.csv

# Load data to target
pipex load "Local File" config.yaml clean_data.csv
```

### 3. Configuration Validation

```bash
# Validate configuration file
pipex validate config.yaml

# Check system status
pipex info
```

## 📋 Configuration Examples

### API to S3 Pipeline

```yaml
extract:
  source: "api"
  connection_details:
    headers:
      Authorization: "Bearer ${API_TOKEN}"
    timeout: 30
  query_or_endpoint: "${API_ENDPOINT}"

transform:
  script: "transform_script.py"
  config:
    drop_columns: ["id"]
    rename_columns:
      title: "post_title"
    filter_rows: "post_title.notna()"
    add_columns:
      processed_date: "pd.Timestamp.now()"

load:
  target: "S3 Bucket"
  config:
    aws_access_key_id: "${AWS_ACCESS_KEY_ID}"
    aws_secret_access_key: "${AWS_SECRET_ACCESS_KEY}"
    region_name: "${AWS_REGION}"
    bucket_name: "${BUCKET_NAME}"
    file_name: "processed_data.csv"
```

### Database to Database Pipeline

```yaml
extract:
  source: "database"
  connection_details:
    db_type: "postgres"
    host: "${DB_HOST}"
    user: "${DB_USER}"
    password: "${DB_PASSWORD}"
    database: "${DB_NAME}"
  query_or_endpoint: "SELECT * FROM users WHERE active = true"

transform:
  config:
    drop_columns: ["password_hash"]
    add_columns:
      full_name: "first_name + ' ' + last_name"

load:
  target: "database"
  config:
    db_type: "mysql"
    host: "${TARGET_DB_HOST}"
    username: "${TARGET_DB_USER}"
    password: "${TARGET_DB_PASSWORD}"
    database: "${TARGET_DB_NAME}"
    table_name: "active_users"
```

### File Processing Pipeline

```yaml
extract:
  source: "file"
  connection_details:
    file_type: "csv"
    encoding: "utf-8"
  query_or_endpoint: "input_data.csv"

transform:
  config:
    filter_rows: "age >= 18"
    add_columns:
      is_adult: "True"

load:
  target: "Local File"
  config:
    file_type: "json"
    file_path: "output/adults.json"
```

## 🐍 Custom Transformation Scripts

### Basic Transformation Script

```python
import pandas as pd

def transform(data: pd.DataFrame) -> pd.DataFrame:
    # Clean data
    data = data.dropna()

    # Add computed columns
    data['processed_date'] = pd.Timestamp.now()

    # Apply business logic
    if 'score' in data.columns:
        data['grade'] = data['score'].apply(
            lambda x: 'A' if x >= 90 else 'B' if x >= 80 else 'C'
        )

    return data
```

### Advanced Transformation Script

```python
import pandas as pd
import numpy as np

def transform(data: pd.DataFrame) -> pd.DataFrame:
    # Data cleaning
    data = data.drop_duplicates()
    data = data.fillna(method='ffill')

    # Feature engineering
    if 'date' in data.columns:
        data['date'] = pd.to_datetime(data['date'])
        data['year'] = data['date'].dt.year
        data['month'] = data['date'].dt.month

    # Statistical features
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        data[f'{col}_zscore'] = (data[col] - data[col].mean()) / data[col].std()

    return data
```

## 🌍 Environment Variables

Create a `.env` file with your credentials:

```bash
# API Configuration
API_TOKEN=your-api-token
API_ENDPOINT=https://api.example.com/data

# AWS Configuration
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=us-east-1
BUCKET_NAME=your-bucket

# Database Configuration
DB_HOST=localhost
DB_USER=username
DB_PASSWORD=password
DB_NAME=database
```

## 🔧 Advanced Usage

### Batch Processing Multiple Files

```bash
# Process multiple files in sequence
for file in data/*.csv; do
    pipex extract file config.yaml --output "processed_$(basename $file)"
done
```

### Pipeline Monitoring

```bash
# Run with verbose logging and save to file
pipex run --config config.yaml --verbose 2>&1 | tee pipeline.log

# Check for errors
grep "ERROR" pipeline.log
```

### Configuration Testing

```bash
# Test different configurations
pipex validate config_dev.yaml
pipex validate config_prod.yaml

# Dry run before production
pipex run --config config_prod.yaml --dry-run
```

## 🚨 Error Handling

### Common Issues and Solutions

1. **Missing Environment Variables**

   ```bash
   # Check what's missing
   pipex info

   # Set missing variables
   export API_TOKEN="your-token"
   ```

2. **Configuration Errors**

   ```bash
   # Validate configuration
   pipex validate config.yaml

   # Check specific sections
   pipex run --dry-run
   ```

3. **Data Processing Errors**

   ```bash
   # Run with verbose logging
   pipex run --verbose

   # Test individual stages
   pipex extract api config.yaml --output test.csv
   ```

## 📊 Performance Tips

1. **Use appropriate data types** in transformations
2. **Filter data early** to reduce processing time
3. **Use batch processing** for large datasets
4. **Monitor memory usage** with the info command
5. **Cache API responses** when possible

## 🔄 Integration Examples

### Cron Job Scheduling

```bash
# Add to crontab for daily execution
0 2 * * * cd /path/to/pipex && pipex run --config daily_pipeline.yaml
```

### Docker Integration

```dockerfile
FROM python:3.11
COPY . /app
WORKDIR /app
RUN pip install -e .
CMD ["pipex", "run", "--config", "config.yaml"]
```

### CI/CD Pipeline

```yaml
# GitHub Actions example
- name: Run ETL Pipeline
  run: |
    pipex validate config.yaml
    pipex run --config config.yaml --dry-run
    pipex run --config config.yaml
```
