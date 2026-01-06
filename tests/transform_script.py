"""
Example transformation script for PipeX ETL pipeline.

This script demonstrates how to create custom transformations for your data.
The transform function is the entry point that PipeX will call.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


def transform(data: pd.DataFrame) -> pd.DataFrame:
    """
    Apply custom transformations to the DataFrame.
    
    This function is called by PipeX during the transformation stage.
    You can implement any custom logic here using pandas operations.
    
    Parameters:
        data (pd.DataFrame): Input DataFrame to be transformed.
    
    Returns:
        pd.DataFrame: Transformed DataFrame.
    """
    logger.info("Starting custom transformations...")
    original_shape = data.shape
    
    try:
        # 1. Data cleaning
        data = clean_data(data)
        
        # 2. Feature engineering
        data = add_features(data)
        
        # 3. Data validation
        data = validate_and_fix_data(data)
        
        final_shape = data.shape
        logger.info(f"Transformation complete: {original_shape} -> {final_shape}")
        
        return data
        
    except Exception as e:
        logger.error(f"Error in custom transformation: {str(e)}")
        raise


def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize the data."""
    logger.info("Cleaning data...")
    
    # Remove duplicate rows
    initial_rows = len(data)
    data = data.drop_duplicates()
    if len(data) < initial_rows:
        logger.info(f"Removed {initial_rows - len(data)} duplicate rows")
    
    # Handle missing values
    for column in data.columns:
        if data[column].dtype == 'object':
            # Fill missing strings with empty string
            data[column] = data[column].fillna('')
        elif data[column].dtype in ['int64', 'float64']:
            # Fill missing numbers with median
            median_val = data[column].median()
            data[column] = data[column].fillna(median_val)
    
    # Standardize text columns
    text_columns = data.select_dtypes(include=['object']).columns
    for col in text_columns:
        if col in data.columns:
            # Strip whitespace and convert to lowercase
            data[col] = data[col].astype(str).str.strip().str.lower()
    
    return data


def add_features(data: pd.DataFrame) -> pd.DataFrame:
    """Add computed features to the dataset."""
    logger.info("Adding computed features...")
    
    # Example: If we have a 'title' column, add title-related features
    if 'title' in data.columns:
        data['title_length'] = data['title'].str.len()
        data['title_word_count'] = data['title'].str.split().str.len()
        data['title_has_numbers'] = data['title'].str.contains(r'\d', na=False)
    
    # Example: If we have 'content' column, add content features
    if 'content' in data.columns:
        data['content_length'] = data['content'].str.len()
        data['content_word_count'] = data['content'].str.split().str.len()
        data['content_paragraph_count'] = data['content'].str.count('\n\n') + 1
    
    # Example: If we have numeric columns, add statistical features
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    if len(numeric_columns) > 1:
        # Add a composite score (example)
        data['composite_score'] = data[numeric_columns].mean(axis=1)
    
    # Add timestamp for when the transformation was applied
    data['processed_timestamp'] = pd.Timestamp.now()
    
    return data


def validate_and_fix_data(data: pd.DataFrame) -> pd.DataFrame:
    """Validate data quality and fix common issues."""
    logger.info("Validating and fixing data...")
    
    # Remove rows with all NaN values
    data = data.dropna(how='all')
    
    # Fix data types
    for column in data.columns:
        # Try to convert string numbers to numeric
        if data[column].dtype == 'object':
            # Check if column contains only numeric strings
            try:
                numeric_data = pd.to_numeric(data[column], errors='coerce')
                if not numeric_data.isna().all():
                    # If more than 50% of values are numeric, convert the column
                    if (numeric_data.notna().sum() / len(data)) > 0.5:
                        data[column] = numeric_data
                        logger.info(f"Converted column '{column}' to numeric")
            except:
                pass
    
    # Ensure no infinite values
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    for col in numeric_columns:
        if np.isinf(data[col]).any():
            data[col] = data[col].replace([np.inf, -np.inf], np.nan)
            data[col] = data[col].fillna(data[col].median())
            logger.info(f"Fixed infinite values in column '{col}'")
    
    return data


def custom_business_logic(data: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
    """
    Apply custom business logic based on configuration.
    
    This function demonstrates how you can use configuration parameters
    to customize transformations.
    """
    logger.info("Applying custom business logic...")
    
    # Example: Apply business rules based on config
    if config.get('apply_business_rules', False):
        # Example business rule: Flag high-value items
        if 'value' in data.columns:
            threshold = config.get('high_value_threshold', 1000)
            data['is_high_value'] = data['value'] > threshold
        
        # Example: Categorize items
        if 'score' in data.columns:
            data['score_category'] = pd.cut(
                data['score'], 
                bins=[0, 30, 70, 100], 
                labels=['low', 'medium', 'high']
            )
    
    return data


# Example usage and testing
if __name__ == "__main__":
    # Configure logging for testing
    logging.basicConfig(level=logging.INFO)
    
    # Create sample dataset for testing
    sample_data = pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'title': ['First Post', '', 'Third Post', 'Fourth Post', 'Fifth Post'],
        'content': ['Short content', 'Medium length content here', '', 'Very long content with multiple sentences and paragraphs.', 'Another post'],
        'views': [100, 200, 300, 400, 500],
        'score': [85, 45, 92, 67, 78],
        'value': [500, 1500, 750, 2000, 300]
    })
    
    print("Original Data:")
    print(sample_data)
    print(f"Shape: {sample_data.shape}")
    print(f"Data types:\n{sample_data.dtypes}")
    
    # Apply transformations
    try:
        transformed_data = transform(sample_data)
        
        print("\nTransformed Data:")
        print(transformed_data)
        print(f"Shape: {transformed_data.shape}")
        print(f"New columns: {set(transformed_data.columns) - set(sample_data.columns)}")
        
    except Exception as e:
        print(f"Error during transformation: {e}")
        raise
