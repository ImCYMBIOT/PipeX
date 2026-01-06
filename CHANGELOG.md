# Changelog

All notable changes to PipeX will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - 2026-01-06

### Added

- **Multi-Cloud Storage Support**: AWS S3, Google Cloud Storage, Azure Blob Storage, DigitalOcean Spaces
- **Enhanced File Format Support**: Excel (.xlsx, .xls), Parquet, XML, enhanced CSV/JSON
- **Intelligent Error Handling**: User-friendly messages with actionable solutions
- **Advanced Transformation System**: Multiple script execution, default transforms library
- **Industry-Specific Templates**: Finance, Retail, Healthcare, Manufacturing transformations
- **Performance Optimization**: Chunked processing for large datasets (100K+ rows)
- **Data Profiling**: Comprehensive data quality analysis and reporting
- **Configurable Validation Rules**: Flexible data validation with multiple rule types
- **Enhanced Feature Engineering**: Text features, numeric aggregates, interaction features
- **Automatic Directory Creation**: Output files organized in timestamped folders
- **Modular Installation**: Optional dependencies for cloud providers and file formats

### Enhanced

- **Default Transforms**: Completely rewritten with better configurability and performance
- **Error Messages**: Context-aware guidance with technical details and solutions
- **Configuration System**: Nested configuration with granular control
- **Logging**: Structured logging with transformation summaries and progress tracking
- **Memory Efficiency**: Chunked processing and optimized data handling
- **Type Safety**: Comprehensive type hints and validation

### Changed

- **Breaking**: Configuration structure updated for better organization
- **Breaking**: Transform function signatures updated for consistency
- **Breaking**: Minimum Python version raised to 3.11
- **Installation**: Now supports `pipex[aws]`, `pipex[gcp]`, `pipex[azure]`, `pipex[all]`

### Fixed

- **AWS Parameter Typo**: Fixed critical security vulnerability in S3 configuration
- **Memory Leaks**: Improved DataFrame copying and memory management
- **Error Handling**: Robust error recovery and user guidance
- **Data Safety**: All transforms now work on DataFrame copies

### Security

- **Credential Management**: Enhanced security for multi-cloud authentication
- **Input Validation**: Comprehensive validation to prevent injection attacks
- **Error Sanitization**: Sensitive information removed from error messages

## [1.0.0] - 2024-12-01

### Added

- Initial release of PipeX CLI tool
- Basic ETL pipeline functionality
- AWS S3 integration
- CSV and JSON file support
- Configuration-based transformations
- Command-line interface with Typer

### Features

- API data extraction with authentication
- Database connectivity (MySQL, PostgreSQL, MongoDB)
- Custom Python transformation scripts
- Environment variable substitution
- Comprehensive logging
- Dry-run mode for testing
