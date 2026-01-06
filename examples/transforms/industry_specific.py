"""
Industry-specific transformation examples for PipeX.

This script demonstrates how to create transformations
tailored to specific industries and use cases.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


def transform(data: pd.DataFrame, config: dict = None) -> pd.DataFrame:
    """
    Apply industry-specific transformations based on configuration.
    
    Args:
        data: Input DataFrame
        config: Configuration dictionary with industry and rules
        
    Returns:
        Transformed DataFrame
    """
    config = config or {}
    industry = config.get('industry', 'general').lower()
    
    logger.info(f"Applying {industry} industry transformations...")
    
    if industry == 'finance':
        return finance_transforms(data, config)
    elif industry == 'retail':
        return retail_transforms(data, config)
    elif industry == 'healthcare':
        return healthcare_transforms(data, config)
    elif industry == 'manufacturing':
        return manufacturing_transforms(data, config)
    else:
        return general_transforms(data, config)


def finance_transforms(data: pd.DataFrame, config: dict) -> pd.DataFrame:
    """Financial industry specific transformations."""
    logger.info("Applying financial industry transformations...")
    
    # Transaction amount processing
    if 'amount' in data.columns:
        # Flag large transactions
        large_threshold = config.get('large_transaction_threshold', 10000)
        data['is_large_transaction'] = data['amount'] > large_threshold
        
        # Calculate log amount for analysis
        data['amount_log'] = np.log1p(data['amount'].abs())
        
        # Risk scoring based on amount
        data['risk_score'] = np.where(
            data['amount'] > large_threshold, 'HIGH',
            np.where(data['amount'] > 1000, 'MEDIUM', 'LOW')
        )
    
    # Date processing for financial data
    if 'transaction_date' in data.columns:
        data['transaction_date'] = pd.to_datetime(data['transaction_date'])
        data['is_business_day'] = data['transaction_date'].dt.dayofweek < 5
        data['quarter'] = data['transaction_date'].dt.quarter
        data['fiscal_year'] = np.where(
            data['transaction_date'].dt.month >= 4,
            data['transaction_date'].dt.year + 1,
            data['transaction_date'].dt.year
        )
    
    # Account type classification
    if 'account_number' in data.columns:
        data['account_type'] = data['account_number'].astype(str).str[:2].map({
            '10': 'CHECKING',
            '20': 'SAVINGS',
            '30': 'CREDIT',
            '40': 'INVESTMENT'
        }).fillna('OTHER')
    
    # Compliance flags
    if config.get('compliance_checks', True):
        # Flag potential money laundering (multiple large transactions)
        if 'customer_id' in data.columns and 'amount' in data.columns:
            customer_stats = data.groupby('customer_id')['amount'].agg(['sum', 'count', 'max']).reset_index()
            customer_stats.columns = ['customer_id', 'total_amount', 'transaction_count', 'max_amount']
            
            # Flag suspicious activity
            customer_stats['suspicious_activity'] = (
                (customer_stats['total_amount'] > 50000) |
                (customer_stats['transaction_count'] > 100) |
                (customer_stats['max_amount'] > 25000)
            )
            
            data = data.merge(customer_stats[['customer_id', 'suspicious_activity']], 
                            on='customer_id', how='left')
    
    return data


def retail_transforms(data: pd.DataFrame, config: dict) -> pd.DataFrame:
    """Retail industry specific transformations."""
    logger.info("Applying retail industry transformations...")
    
    # Product and pricing analysis
    if 'price' in data.columns and 'quantity' in data.columns:
        data['total_value'] = data['price'] * data['quantity']
        data['unit_margin'] = data.get('selling_price', data['price']) - data.get('cost_price', 0)
        data['total_margin'] = data['unit_margin'] * data['quantity']
    
    # Customer segmentation
    if 'customer_id' in data.columns:
        customer_metrics = data.groupby('customer_id').agg({
            'total_value': ['sum', 'mean', 'count'],
            'quantity': 'sum'
        }).reset_index()
        
        customer_metrics.columns = [
            'customer_id', 'customer_total_spend', 'customer_avg_order', 
            'customer_order_count', 'customer_total_items'
        ]
        
        # Customer lifetime value estimation
        customer_metrics['estimated_clv'] = (
            customer_metrics['customer_avg_order'] * 
            customer_metrics['customer_order_count'] * 2  # Simple 2x multiplier
        )
        
        # Customer tier classification
        customer_metrics['customer_tier'] = pd.cut(
            customer_metrics['customer_total_spend'],
            bins=[0, 100, 500, 2000, float('inf')],
            labels=['BRONZE', 'SILVER', 'GOLD', 'PLATINUM']
        )
        
        data = data.merge(customer_metrics, on='customer_id', how='left')
    
    # Seasonal analysis
    if 'order_date' in data.columns:
        data['order_date'] = pd.to_datetime(data['order_date'])
        data['season'] = data['order_date'].dt.month.map({
            12: 'WINTER', 1: 'WINTER', 2: 'WINTER',
            3: 'SPRING', 4: 'SPRING', 5: 'SPRING',
            6: 'SUMMER', 7: 'SUMMER', 8: 'SUMMER',
            9: 'FALL', 10: 'FALL', 11: 'FALL'
        })
        data['is_holiday_season'] = data['order_date'].dt.month.isin([11, 12])
    
    # Product category analysis
    if 'product_category' in data.columns:
        category_stats = data.groupby('product_category')['total_value'].agg(['mean', 'std']).reset_index()
        category_stats.columns = ['product_category', 'category_avg_value', 'category_value_std']
        data = data.merge(category_stats, on='product_category', how='left')
        
        # Flag high-value categories
        data['is_premium_category'] = data['category_avg_value'] > data['category_avg_value'].quantile(0.8)
    
    return data


def healthcare_transforms(data: pd.DataFrame, config: dict) -> pd.DataFrame:
    """Healthcare industry specific transformations."""
    logger.info("Applying healthcare industry transformations...")
    
    # Patient demographics
    if 'birth_date' in data.columns:
        data['birth_date'] = pd.to_datetime(data['birth_date'])
        data['age'] = (datetime.now() - data['birth_date']).dt.days / 365.25
        
        # Age group classification
        data['age_group'] = pd.cut(
            data['age'],
            bins=[0, 18, 35, 50, 65, 100],
            labels=['PEDIATRIC', 'YOUNG_ADULT', 'ADULT', 'MIDDLE_AGE', 'SENIOR']
        )
    
    # Medical coding and classification
    if 'diagnosis_code' in data.columns:
        # ICD-10 code processing (simplified)
        data['diagnosis_category'] = data['diagnosis_code'].astype(str).str[:3]
        data['is_chronic_condition'] = data['diagnosis_code'].astype(str).str.startswith(('E', 'I', 'N'))
    
    # Treatment duration and outcomes
    if 'admission_date' in data.columns and 'discharge_date' in data.columns:
        data['admission_date'] = pd.to_datetime(data['admission_date'])
        data['discharge_date'] = pd.to_datetime(data['discharge_date'])
        data['length_of_stay'] = (data['discharge_date'] - data['admission_date']).dt.days
        
        # Flag extended stays
        data['extended_stay'] = data['length_of_stay'] > config.get('extended_stay_threshold', 7)
    
    # Risk stratification
    if 'age' in data.columns and 'diagnosis_category' in data.columns:
        # Simple risk scoring
        risk_factors = 0
        risk_factors += np.where(data['age'] > 65, 2, 0)
        risk_factors += np.where(data['is_chronic_condition'], 1, 0)
        risk_factors += np.where(data.get('length_of_stay', 0) > 7, 1, 0)
        
        data['risk_score'] = risk_factors
        data['risk_level'] = pd.cut(
            data['risk_score'],
            bins=[-1, 0, 2, 4, 10],
            labels=['LOW', 'MODERATE', 'HIGH', 'CRITICAL']
        )
    
    return data


def manufacturing_transforms(data: pd.DataFrame, config: dict) -> pd.DataFrame:
    """Manufacturing industry specific transformations."""
    logger.info("Applying manufacturing industry transformations...")
    
    # Production metrics
    if 'production_date' in data.columns:
        data['production_date'] = pd.to_datetime(data['production_date'])
        data['shift'] = data['production_date'].dt.hour.map(lambda x: 
            'NIGHT' if x < 6 or x >= 22 else 'DAY' if x < 14 else 'EVENING'
        )
        data['weekday'] = data['production_date'].dt.day_name()
        data['is_weekend'] = data['production_date'].dt.dayofweek >= 5
    
    # Quality metrics
    if 'defect_count' in data.columns and 'total_produced' in data.columns:
        data['defect_rate'] = data['defect_count'] / data['total_produced']
        data['quality_grade'] = pd.cut(
            data['defect_rate'],
            bins=[0, 0.01, 0.05, 0.1, 1.0],
            labels=['EXCELLENT', 'GOOD', 'ACCEPTABLE', 'POOR']
        )
    
    # Equipment efficiency
    if 'runtime_hours' in data.columns and 'planned_hours' in data.columns:
        data['efficiency'] = data['runtime_hours'] / data['planned_hours']
        data['downtime_hours'] = data['planned_hours'] - data['runtime_hours']
        data['needs_maintenance'] = data['efficiency'] < config.get('efficiency_threshold', 0.85)
    
    # Cost analysis
    if 'material_cost' in data.columns and 'labor_cost' in data.columns:
        data['total_cost'] = data['material_cost'] + data['labor_cost'] + data.get('overhead_cost', 0)
        if 'total_produced' in data.columns:
            data['cost_per_unit'] = data['total_cost'] / data['total_produced']
    
    return data


def general_transforms(data: pd.DataFrame, config: dict) -> pd.DataFrame:
    """General purpose transformations for any industry."""
    logger.info("Applying general transformations...")
    
    # Basic data quality improvements
    data = data.drop_duplicates()
    
    # Add processing metadata
    data['processed_at'] = datetime.now()
    data['data_source'] = config.get('data_source', 'unknown')
    
    # Basic feature engineering
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    if len(numeric_columns) > 1:
        data['numeric_sum'] = data[numeric_columns].sum(axis=1)
        data['numeric_mean'] = data[numeric_columns].mean(axis=1)
    
    return data


if __name__ == "__main__":
    # Test the transformations
    test_data = pd.DataFrame({
        'customer_id': [1, 2, 3, 1, 2],
        'amount': [100, 15000, 500, 200, 25000],
        'transaction_date': ['2024-01-15', '2024-01-16', '2024-01-17', '2024-01-18', '2024-01-19'],
        'account_number': ['1001234', '2005678', '3009012', '1001234', '2005678']
    })
    
    config = {
        'industry': 'finance',
        'large_transaction_threshold': 10000,
        'compliance_checks': True
    }
    
    result = transform(test_data, config)
    print("Transformed data:")
    print(result.head())
    print(f"New columns: {set(result.columns) - set(test_data.columns)}")