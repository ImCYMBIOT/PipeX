import typer
import yaml
import pandas as pd
import json
import os
from dotenv import load_dotenv

from app.load import load_data
from app.extract import extract_data
from app.transform import transform_data

load_dotenv()  # Load environment variables from .env file

app = typer.Typer()

@app.command()
def extract(source: str, config: str):
    typer.echo(f"Extracting data from {source} using config: {config}")
    with open(config, 'r') as file:
        config_data = yaml.safe_load(file)
    
    data = extract_data(
        source_type=source,
        connection_details=config_data['extract']['connection_details'],
        query_or_endpoint=config_data['extract']['query_or_endpoint']
    )
    typer.echo("Data extraction complete.")
    data_json = data.to_json(orient='split')
    return data_json

@app.command()
def transform(script: str, config: str, data_json: str):
    typer.echo(f"Transforming data using script: {script} and config: {config}")
    with open(config, 'r') as file:
        config_data = yaml.safe_load(file)
    
    data = pd.read_json(data_json, orient='split')
    transformed_data = transform_data(script, config_data, data)
    typer.echo("Data transformation complete.")
    transformed_data_json = transformed_data.to_json(orient='split')
    return transformed_data_json

@app.command()
def load(target: str, config: str, data_json: str):
    typer.echo(f"Loading data to {target} using config: {config}")
    with open(config, 'r') as file:
        config_data = yaml.safe_load(file)
    
    # Replace environment variable placeholders with actual values
    config_data['load']['config']['aws_access_key_id'] = os.getenv('AWS_ACCESS_KEY_ID')
    config_data['load']['config']['aws_secret_access_key'] = os.getenv('AWS_SECRET_ACCESS_KEY')
    
    data = pd.read_json(data_json, orient='split')
    load_data(target, config_data, data)
    typer.echo("Data loading complete.")

@app.command()
def run(config: str = "config.yaml"):
    typer.echo(f"Running ETL pipeline with config: {config}")
    with open(config, 'r') as file:
        config_data = yaml.safe_load(file)
    
    # Extract
    typer.echo("Extracting data...")
    data_json = extract(
        source=config_data['extract']['source'],
        config=config
    )
    
    # Transform
    typer.echo("Transforming data...")
    transformed_data_json = transform(
        script=config_data['transform']['script'],
        config=config,
        data_json=data_json
    )
    
    # Load
    typer.echo("Loading data...")
    load(
        target=config_data['load']['target'],
        config=config,
        data_json=transformed_data_json
    )

if __name__ == "__main__":
    app()