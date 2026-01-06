"""
Performance benchmarks for PipeX default transforms.
"""

import pytest
import pandas as pd
import numpy as np
from app.default_transforms import transform, clean_data, feature_engineering


@pytest.fixture
def sample_data():
    """Generate sample data for benchmarking."""
    np.random.seed(42)
    return pd.DataFrame({
        'id': range(1000),
        'name': [f'User_{i}' for i in range(1000)],
        'value': np.random.randn(1000),
        'category': np.random.choice(['A', 'B', 'C'], 1000),
        'date': pd.date_range('2023-01-01', periods=1000, freq='D')
    })


@pytest.fixture
def large_data():
    """Generate larger dataset for performance testing."""
    np.random.seed(42)
    return pd.DataFrame({
        'id': range(10000),
        'name': [f'User_{i}' for i in range(10000)],
        'value': np.random.randn(10000),
        'category': np.random.choice(['A', 'B', 'C', 'D', 'E'], 10000),
        'date': pd.date_range('2023-01-01', periods=10000, freq='H')
    })


def test_clean_data_performance(benchmark, sample_data):
    """Benchmark clean_data function."""
    config = {
        'remove_duplicates': True,
        'missing_strategy': 'fill',
        'standardize_text': True
    }
    
    result = benchmark(clean_data, sample_data, config)
    assert len(result) <= len(sample_data)


def test_feature_engineering_performance(benchmark, sample_data):
    """Benchmark feature_engineering function."""
    config = {
        'add_text_features': True,
        'add_numeric_features': True,
        'add_date_features': True
    }
    
    result = benchmark(feature_engineering, sample_data, config)
    assert result.shape[1] > sample_data.shape[1]  # Should add columns


def test_full_transform_performance(benchmark, sample_data):
    """Benchmark full transform pipeline."""
    config = {
        'clean_data': True,
        'feature_engineering': True,
        'add_metadata': True
    }
    
    result = benchmark(transform, sample_data, config)
    assert len(result) > 0


def test_chunked_processing_performance(benchmark, large_data):
    """Benchmark chunked processing for large datasets."""
    config = {
        'chunk_threshold': 5000,
        'chunk_size': 2500,
        'clean_data': True
    }
    
    result = benchmark(clean_data, large_data, config)
    assert len(result) <= len(large_data)


@pytest.mark.parametrize("data_size", [100, 1000, 5000])
def test_scalability(data_size):
    """Test performance scaling with different data sizes."""
    np.random.seed(42)
    data = pd.DataFrame({
        'id': range(data_size),
        'value': np.random.randn(data_size),
        'category': np.random.choice(['A', 'B', 'C'], data_size)
    })
    
    config = {'clean_data': True, 'add_metadata': True}
    result = transform(data, config)
    
    # Should complete in reasonable time
    assert len(result) <= data_size
    assert result.shape[1] >= data.shape[1]  # Should add metadata columns