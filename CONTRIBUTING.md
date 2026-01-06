# Contributing to PipeX

Thank you for your interest in contributing to PipeX! This document provides guidelines and information for contributors.

## 🚀 Quick Start

### Development Setup

1. **Fork and clone the repository**

```bash
git clone https://github.com/yourusername/pipex.git
cd pipex
```

2. **Set up development environment**

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with all dependencies
pip install -e .[all,dev]
```

3. **Install pre-commit hooks**

```bash
pip install pre-commit
pre-commit install
```

## 📋 Development Guidelines

### Code Style

We use automated code formatting and linting:

- **Black** for code formatting (line length: 127)
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

```bash
# Format code
black app/ tests/
isort app/ tests/

# Check linting
flake8 app/ tests/
mypy app/
```

### Testing

We maintain high test coverage and quality:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run performance benchmarks
pytest tests/test_performance.py --benchmark-only

# Run specific test categories
pytest -m "not integration"  # Skip integration tests
```

### Documentation

- Update docstrings for all public functions
- Add type hints to all function signatures
- Update README.md for user-facing changes
- Add examples for new features

## 🎯 Contribution Areas

### High Priority

- **New Cloud Providers**: IBM Cloud, Oracle Cloud, Alibaba Cloud
- **Additional File Formats**: Avro, ORC, HDF5, Feather
- **Database Connectors**: Snowflake, BigQuery, Redshift
- **Transformation Functions**: More industry-specific templates
- **Performance Optimization**: Parallel processing, streaming

### Medium Priority

- **Data Quality**: Advanced validation rules and profiling
- **Monitoring**: Metrics collection and alerting
- **Security**: Enhanced authentication and encryption
- **CLI Improvements**: Interactive mode, better help system
- **Documentation**: Video tutorials, advanced examples

### Always Welcome

- **Bug fixes** and error handling improvements
- **Test coverage** improvements
- **Documentation** updates and examples
- **Performance** optimizations
- **Code quality** improvements

## 🔄 Contribution Process

### 1. Planning

- **Check existing issues** before starting work
- **Create an issue** for new features or significant changes
- **Discuss approach** in the issue comments
- **Get approval** for major changes before implementation

### 2. Development

- **Create feature branch** from `main`

```bash
git checkout -b feature/your-feature-name
```

- **Follow coding standards** and write tests
- **Commit with clear messages**

```bash
git commit -m "feat: add support for Oracle Cloud Storage

- Implement OracleCloudProvider class
- Add authentication with API keys
- Include comprehensive error handling
- Add configuration examples and tests

Closes #123"
```

### 3. Testing

- **Write comprehensive tests** for new functionality
- **Ensure all tests pass** locally
- **Add integration tests** for external services (when possible)
- **Update performance benchmarks** if applicable

### 4. Documentation

- **Update docstrings** and type hints
- **Add configuration examples** for new features
- **Update README.md** if user-facing changes
- **Add to CHANGELOG.md** following format

### 5. Pull Request

- **Create PR** with clear title and description
- **Link related issues** using "Closes #123"
- **Request review** from maintainers
- **Address feedback** promptly

## 📝 Commit Message Format

We follow conventional commits for automated changelog generation:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Types:**

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**

```bash
feat(cloud): add Google Cloud Storage support
fix(transforms): handle empty DataFrames in clean_data
docs(readme): update installation instructions
test(api): add integration tests for authentication
```

## 🏗️ Architecture Guidelines

### Code Organization

```
app/
├── cli.py              # Command-line interface
├── extract.py          # Data extraction logic
├── transform.py        # Transformation orchestration
├── load.py            # Data loading logic
├── cloud_storage.py   # Multi-cloud storage providers
├── default_transforms.py  # Default transformation library
├── error_handler.py   # Error handling and user guidance
└── utils.py           # Utility functions

tests/
├── test_*.py          # Unit tests
├── test_integration.py # Integration tests
└── test_performance.py # Performance benchmarks
```

### Design Principles

- **Modularity**: Each module has a single responsibility
- **Extensibility**: Easy to add new providers, formats, transforms
- **Configuration**: Everything configurable via YAML
- **Error Handling**: User-friendly messages with actionable guidance
- **Performance**: Efficient processing for large datasets
- **Security**: Secure credential management and input validation

### Adding New Features

#### New Cloud Provider

1. Create provider class inheriting from `CloudStorageProvider`
2. Implement required methods: `upload_file`, `download_file`, `list_files`
3. Add authentication handling and error management
4. Update `get_cloud_provider` factory function
5. Add configuration examples and tests

#### New File Format

1. Add format detection in `extract.py` and `load.py`
2. Implement read/write functions with error handling
3. Add format-specific configuration options
4. Update documentation and examples
5. Add comprehensive tests

#### New Transformation

1. Add function to `default_transforms.py` or create new module
2. Follow existing patterns for configuration and error handling
3. Add to industry-specific templates if applicable
4. Include comprehensive docstring and type hints
5. Add unit tests and performance benchmarks

## 🐛 Bug Reports

When reporting bugs, please include:

- **PipeX version** (`pipex --version`)
- **Python version** and operating system
- **Complete error message** and stack trace
- **Configuration file** (sanitized of credentials)
- **Steps to reproduce** the issue
- **Expected vs actual behavior**

## 💡 Feature Requests

For feature requests, please provide:

- **Use case description** and business value
- **Proposed solution** or implementation approach
- **Alternative solutions** considered
- **Examples** of how it would be used
- **Willingness to contribute** implementation

## 📞 Getting Help

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and community support
- **Email**: agniveshkumar15@gmail.com for security issues

## 🏆 Recognition

Contributors are recognized in:

- **CONTRIBUTORS.md** file
- **GitHub releases** changelog
- **README.md** acknowledgments section

Thank you for helping make PipeX better! 🚀
