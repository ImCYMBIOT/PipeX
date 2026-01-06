"""
PipeX - A powerful CLI-based ETL pipeline automation tool.

This package provides comprehensive ETL functionality including:
- Data extraction from APIs, databases, and files (CSV, JSON, Excel, Parquet, XML)
- Data transformation with custom scripts and configurations
- Data loading to various targets (Local files, AWS S3, GCP, Azure, DigitalOcean)
- Multi-cloud storage support
- Advanced error handling with user guidance
- Industry-specific transformation templates
- Robust error handling and logging
- Environment variable management
"""

import logging

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Setup basic logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

from .api import APIClient

# Import new modules
from .cloud_storage import download_from_cloud, get_cloud_provider, upload_to_cloud
from .default_transforms import add_metadata, clean_data, data_validation, feature_engineering
from .default_transforms import transform as default_transform
from .error_handler import ErrorHandler, PipeXError, handle_pipeline_error

# Import main functions
from .extract import extract_data
from .load import load_data
from .storage import download_from_s3, file_exists_in_s3, save_and_upload, save_to_file, upload_to_s3
from .transform import transform_data
from .utils import apply_env_variables, get_env_variable, load_config, setup_logging, validate_config, validate_data_schema

__version__ = "0.2.0"

__all__ = [
    # Core ETL functions
    "extract_data",
    "transform_data",
    "load_data",
    # Storage functions
    "save_to_file",
    "upload_to_s3",
    "download_from_s3",
    "file_exists_in_s3",
    "save_and_upload",
    # Cloud storage
    "get_cloud_provider",
    "upload_to_cloud",
    "download_from_cloud",
    # API client
    "APIClient",
    # Utility functions
    "setup_logging",
    "load_config",
    "validate_data_schema",
    "get_env_variable",
    "apply_env_variables",
    "validate_config",
    # Default transformations
    "clean_data",
    "add_metadata",
    "feature_engineering",
    "data_validation",
    "default_transform",
    # Error handling
    "PipeXError",
    "ErrorHandler",
    "handle_pipeline_error",
    # Version
    "__version__",
]
