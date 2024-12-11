import typer
import yaml
import pandas as pd
import os
from io import StringIO
from dotenv import load_dotenv
import questionary
from app.load import load_data
from app.extract import extract_data
from app.transform import transform_data

load_dotenv()  # Load environment variables from .env file

app = typer.Typer()

# Interactive Prompt Functions
def prompt_for_extraction_method():
    return questionary.select(
        "How would you like to extract data?",
        choices=["API", "File", "Database (SQL)", "Database (NoSQL)"]
    ).ask()

def prompt_for_loading_method():
    return questionary.select(
        "Where would you like to load the transformed data?",
        choices=["S3 Bucket", "Local File"]
    ).ask()

def prompt_for_aws_credentials():
    aws_access_key_id = questionary.text("Enter your AWS Access Key ID:").ask()
    aws_secret_access_key = questionary.text("Enter your AWS Secret Access Key:", validate=lambda val: len(val) > 0).ask()
    aws_region = questionary.text("Enter your AWS Region:").ask()
    bucket_name = questionary.text("Enter your S3 Bucket Name:").ask()
    return aws_access_key_id, aws_secret_access_key, aws_region, bucket_name


# CLI Commands
@app.command()
def extract(source: str, config: str) -> str:
    """Extract data from the specified source."""
    typer.echo(f"Extracting data from {source} using config: {config}")
    with open(config, 'r') as file:
        config_data = yaml.safe_load(file)
    
    data = extract_data(
        source_type=source,
        connection_details=config_data['extract']['connection_details'],
        query_or_endpoint=config_data['extract']['query_or_endpoint']
    )
    typer.echo("Data extraction complete.")
    return data.to_json(orient='split')


@app.command()
def transform(script: str, config: str, data_json: str) -> str:
    """Transform data using the specified script and configuration."""
    typer.echo(f"Transforming data using script: {script} and config: {config}")
    with open(config, 'r') as file:
        config_data = yaml.safe_load(file)
    
    data = pd.read_json(StringIO(data_json), orient='split')
    transformed_data = transform_data(script, config_data, data)
    typer.echo("Data transformation complete.")
    return transformed_data.to_json(orient='split')


@app.command()
def load(target: str, config: str, data_json: str):
    """Load data to the specified target."""
    typer.echo(f"Loading data to {target} using config: {config}")
    with open(config, 'r') as file:
        config_data = yaml.safe_load(file)
    
    # Replace environment variable placeholders
    load_config = config_data['load']['config']
    load_config['aws_access_key_id'] = os.getenv('AWS_ACCESS_KEY_ID')
    load_config['aws_secret_access_key'] = os.getenv('AWS_SECRET_ACCESS_KEY')
    load_config['region_name'] = os.getenv('AWS_REGION')
    load_config['bucket_name'] = os.getenv('BUCKET_NAME')
    
    data = pd.read_json(StringIO(data_json), orient='split')
    load_data(target, load_config, data)
    typer.echo("Data loading complete.")


@app.command()
def run(config: str = "config.yaml"):
    """Run the full ETL pipeline."""
    typer.echo(f"Running ETL pipeline with config: {config}")
    with open(config, 'r') as file:
        config_data = yaml.safe_load(file)
    
    # Interactive Extraction
    extraction_method = prompt_for_extraction_method()
    typer.echo(f"Selected extraction method: {extraction_method}")
    data_json = extract(
        source=config_data['extract']['source'],
        config=config
    )

    # Interactive Transformation
    typer.echo("Transforming data...")
    transformed_data_json = transform(
        script=config_data['transform']['script'],
        config=config,
        data_json=data_json
    )

    # Interactive Loading
    loading_method = prompt_for_loading_method()
    typer.echo(f"Selected loading method: {loading_method}")
    if loading_method == "S3 Bucket":
        aws_access_key_id, aws_secret_access_key, aws_region, bucket_name = prompt_for_aws_credentials()
        os.environ['AWS_ACCESS_KEY_ID'] = aws_access_key_id
        os.environ['AWS_SECRET_ACCESS_KEY'] = aws_secret_access_key
        os.environ['AWS_REGION'] = aws_region
        os.environ['BUCKET_NAME'] = bucket_name

    load(
        target=config_data['load']['target'],
        config=config,
        data_json=transformed_data_json
    )


if __name__ == "__main__":
    app()
