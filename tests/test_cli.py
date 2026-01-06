"""
Tests for PipeX CLI commands.

This module tests the command-line interface functionality including
individual commands and full pipeline execution.
"""

import pytest
import pandas as pd
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
from pathlib import Path
import tempfile
import yaml

from app.cli import app


@pytest.fixture
def runner():
    """Create a CLI test runner."""
    return CliRunner()


@pytest.fixture
def sample_config():
    """Create a sample configuration for testing."""
    return {
        'extract': {
            'source': 'api',
            'connection_details': {
                'headers': {'Authorization': 'Bearer test-token'}
            },
            'query_or_endpoint': 'https://api.example.com/data'
        },
        'transform': {
            'script': 'tests/transform_script.py',
            'config': {
                'drop_columns': ['id'],
                'rename_columns': {'title': 'post_title'},
                'filter_rows': 'post_title != ""',
                'add_columns': {'title_length': 'post_title.str.len()'}
            },
            'options': {
                'drop_columns': True,
                'rename_columns': True,
                'filter_rows': True,
                'add_columns': True
            }
        },
        'load': {
            'target': 'S3 Bucket',
            'config': {
                'aws_access_key_id': 'test-key',
                'aws_secret_access_key': 'test-secret',
                'region_name': 'us-east-1',
                'bucket_name': 'test-bucket',
                'file_name': 'test-data.csv'
            }
        }
    }


@pytest.fixture
def sample_data():
    """Create sample DataFrame for testing."""
    return pd.DataFrame({
        'id': [1, 2, 3],
        'title': ['First Post', 'Second Post', 'Third Post'],
        'content': ['Content 1', 'Content 2', 'Content 3'],
        'views': [100, 200, 300]
    })


@pytest.fixture
def temp_config_file(sample_config):
    """Create a temporary configuration file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(sample_config, f)
        return f.name


def test_extract_command_success(runner, temp_config_file, sample_data):
    """Test successful data extraction command."""
    with patch('app.cli.extract_data') as mock_extract:
        mock_extract.return_value = sample_data
        
        result = runner.invoke(app, [
            'extract', 'api', temp_config_file
        ])
        
        assert result.exit_code == 0
        assert "Starting data extraction from api" in result.output
        assert "Data extraction completed successfully" in result.output
        mock_extract.assert_called_once()


def test_extract_command_with_output_file(runner, temp_config_file, sample_data):
    """Test extraction command with output file."""
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as output_file:
        with patch('app.cli.extract_data') as mock_extract:
            mock_extract.return_value = sample_data
            
            result = runner.invoke(app, [
                'extract', 'api', temp_config_file, '--output', output_file.name
            ])
            
            assert result.exit_code == 0
            assert f"Data saved to: {output_file.name}" in result.output


def test_extract_command_missing_config(runner):
    """Test extraction command with missing configuration file."""
    result = runner.invoke(app, [
        'extract', 'api', 'nonexistent_config.yaml'
    ])
    
    assert result.exit_code == 1
    assert "Configuration file not found" in result.output


def test_transform_command_success(runner, temp_config_file, sample_data):
    """Test successful data transformation command."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as input_file:
        sample_data.to_csv(input_file.name, index=False)
        
        with patch('app.cli.transform_data') as mock_transform:
            mock_transform.return_value = sample_data
            
            result = runner.invoke(app, [
                'transform', 'tests/transform_script.py', temp_config_file, input_file.name
            ])
            
            assert result.exit_code == 0
            assert "Starting data transformation" in result.output
            assert "Data transformation completed successfully" in result.output


def test_load_command_success(runner, temp_config_file, sample_data):
    """Test successful data loading command."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as input_file:
        sample_data.to_csv(input_file.name, index=False)
        
        with patch('app.cli.load_data') as mock_load:
            result = runner.invoke(app, [
                'load', 'S3 Bucket', temp_config_file, input_file.name
            ])
            
            assert result.exit_code == 0
            assert "Starting data loading to S3 Bucket" in result.output
            assert "Data loading completed successfully" in result.output
            mock_load.assert_called_once()


def test_run_command_success(runner, temp_config_file, sample_data):
    """Test successful full pipeline execution."""
    with patch('app.cli.extract_data') as mock_extract, \
         patch('app.cli.transform_data') as mock_transform, \
         patch('app.cli.load_data') as mock_load:
        
        mock_extract.return_value = sample_data
        mock_transform.return_value = sample_data
        
        result = runner.invoke(app, [
            'run', '--config', temp_config_file
        ])
        
        assert result.exit_code == 0
        assert "Starting PipeX ETL Pipeline" in result.output
        assert "Step 1: Extracting data" in result.output
        assert "Step 2: Transforming data" in result.output
        assert "Step 3: Loading data" in result.output
        assert "ETL Pipeline completed successfully" in result.output
        
        mock_extract.assert_called_once()
        mock_transform.assert_called_once()
        mock_load.assert_called_once()


def test_run_command_dry_run(runner, temp_config_file):
    """Test pipeline dry run mode."""
    result = runner.invoke(app, [
        'run', '--config', temp_config_file, '--dry-run'
    ])
    
    assert result.exit_code == 0
    assert "Configuration validation completed successfully" in result.output
    assert "Dry run mode - pipeline not executed" in result.output


def test_run_command_verbose(runner, temp_config_file, sample_data):
    """Test pipeline with verbose logging."""
    with patch('app.cli.extract_data') as mock_extract, \
         patch('app.cli.transform_data') as mock_transform, \
         patch('app.cli.load_data') as mock_load:
        
        mock_extract.return_value = sample_data
        mock_transform.return_value = sample_data
        
        result = runner.invoke(app, [
            'run', '--config', temp_config_file, '--verbose'
        ])
        
        assert result.exit_code == 0


def test_validate_command_success(runner, temp_config_file):
    """Test successful configuration validation."""
    result = runner.invoke(app, [
        'validate', temp_config_file
    ])
    
    assert result.exit_code == 0
    assert "Validating configuration" in result.output
    assert "Configuration validation completed successfully" in result.output


def test_validate_command_missing_sections(runner):
    """Test validation with missing configuration sections."""
    incomplete_config = {'extract': {'source': 'api'}}
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(incomplete_config, f)
        
        result = runner.invoke(app, [
            'validate', f.name
        ])
        
        assert result.exit_code == 1
        assert "Missing required sections" in result.output


def test_info_command(runner):
    """Test info command output."""
    result = runner.invoke(app, ['info'])
    
    assert result.exit_code == 0
    assert "PipeX ETL Pipeline Tool" in result.output
    assert "Version:" in result.output
    assert "Environment Variables:" in result.output


def test_error_handling_extract_failure(runner, temp_config_file):
    """Test error handling during extraction."""
    with patch('app.cli.extract_data') as mock_extract:
        mock_extract.side_effect = Exception("API connection failed")
        
        result = runner.invoke(app, [
            'extract', 'api', temp_config_file
        ])
        
        assert result.exit_code == 1
        assert "Error in extraction stage" in result.output


def test_error_handling_transform_failure(runner, temp_config_file, sample_data):
    """Test error handling during transformation."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as input_file:
        sample_data.to_csv(input_file.name, index=False)
        
        with patch('app.cli.transform_data') as mock_transform:
            mock_transform.side_effect = Exception("Transformation script error")
            
            result = runner.invoke(app, [
                'transform', 'tests/transform_script.py', temp_config_file, input_file.name
            ])
            
            assert result.exit_code == 1
            assert "Error in transformation stage" in result.output


def test_error_handling_load_failure(runner, temp_config_file, sample_data):
    """Test error handling during loading."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as input_file:
        sample_data.to_csv(input_file.name, index=False)
        
        with patch('app.cli.load_data') as mock_load:
            mock_load.side_effect = Exception("S3 upload failed")
            
            result = runner.invoke(app, [
                'load', 'S3 Bucket', temp_config_file, input_file.name
            ])
            
            assert result.exit_code == 1
            assert "Error in loading stage" in result.output


def test_pipeline_error_handling(runner, temp_config_file, sample_data):
    """Test error handling in full pipeline."""
    with patch('app.cli.extract_data') as mock_extract:
        mock_extract.side_effect = Exception("Pipeline failure")
        
        result = runner.invoke(app, [
            'run', '--config', temp_config_file
        ])
        
        assert result.exit_code == 1
        assert "Error in pipeline execution stage" in result.output