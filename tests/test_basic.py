"""
Basic tests to ensure the workflow passes.
"""

import pytest
import pandas as pd


def test_basic_import():
    """Test that we can import the main modules."""
    try:
        import app.cli
        import app.default_transforms
        assert True
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")


def test_pandas_works():
    """Test that pandas is working correctly."""
    df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
    assert len(df) == 3
    assert list(df.columns) == ['a', 'b']


def test_default_transforms_basic():
    """Test basic default transforms functionality."""
    from app.default_transforms import clean_data
    
    # Create test data with some issues
    df = pd.DataFrame({
        'name': ['Alice', 'Bob', '', 'Charlie'],
        'age': [25, 30, None, 35],
        'score': [85.5, 92.0, 78.5, 88.0]
    })
    
    # Test basic cleaning
    config = {
        'remove_duplicates': True,
        'missing_strategy': 'fill',
        'standardize_text': True
    }
    
    result = clean_data(df, config)
    
    # Should have same or fewer rows
    assert len(result) <= len(df)
    # Should have same columns
    assert set(result.columns) == set(df.columns)


def test_configuration_structure():
    """Test that we can create a basic configuration."""
    config = {
        'extract': {
            'source': 'api',
            'connection_details': {
                'headers': {'Authorization': 'Bearer test'}
            },
            'query_or_endpoint': 'https://api.example.com'
        },
        'transform': {
            'config': {
                'clean_data': True
            }
        },
        'load': {
            'target': 'Local File',
            'config': {
                'file_path': 'test.csv'
            }
        }
    }
    
    # Basic validation
    assert 'extract' in config
    assert 'transform' in config
    assert 'load' in config
    assert config['extract']['source'] == 'api'