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

# Centralized Helper Functions
def get_env_variables(config):
    """Retrieve environment variables and apply them to the load configuration."""
    config['aws_access_key_id'] = os.getenv('AWS_ACCESS_KEY_ID')
    config['aws_secret_access_key'] = os.getenv('AWS_SECRET_ACCESS_KEY')
    config['region_name'] = os.getenv('AWS_REGION')
    config['bucket_name'] = os.getenv('BUCKET_NAME')
    missing_vars = [key for key, value in config.items() if not value]
    if missing_vars:
        raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")
    return config


def validate_questionary_input(prompt_result, prompt_type="input"):
    """Validate the result of a questionary prompt."""
    if not prompt_result:
        typer.echo(f"{prompt_type.capitalize()} prompt aborted. Exiting.")
        raise typer.Exit()
    return prompt_result


# Interactive Prompt Functions
def prompt_for_extraction_method():
    return validate_questionary_input(
        questionary.select(
            "How would you like to extract data?",
            choices=["API", "File", "Database (SQL)", "Database (NoSQL)"]
        ).ask(),
        "extraction method"
    )


def prompt_for_loading_method():
    return validate_questionary_input(
        questionary.select(
            "Where would you like to load the transformed data?",
            choices=["S3 Bucket", "Local File"]
        ).ask(),
        "loading method"
    )


def prompt_for_aws_credentials():
    aws_access_key_id = validate_questionary_input(questionary.text("Enter your AWS Access Key ID:").ask())
    aws_secret_access_key = validate_questionary_input(
        questionary.text("Enter your AWS Secret Access Key:", validate=lambda val: len(val) > 0).ask()
    )
    aws_region = validate_questionary_input(questionary.text("Enter your AWS Region:").ask())
    bucket_name = validate_questionary_input(questionary.text("Enter your S3 Bucket Name:").ask())
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

    load_config = get_env_variables(config_data['load']['config'])

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
    extracted_data = extract_data(
        source_type=config_data['extract']['source'],
        connection_details=config_data['extract']['connection_details'],
        query_or_endpoint=config_data['extract']['query_or_endpoint']
    )
    data_json = extracted_data.to_json(orient='split')

    # Interactive Transformation
    typer.echo("Transforming data...")
    transformed_data = transform_data(
        script=config_data['transform']['script'],
        config=config_data['transform']['config'],
        data=pd.read_json(StringIO(data_json), orient='split')
    )
    transformed_data_json = transformed_data.to_json(orient='split')

    # Interactive Loading
    loading_method = prompt_for_loading_method()
    typer.echo(f"Selected loading method: {loading_method}")
    if loading_method == "S3 Bucket":
        aws_access_key_id, aws_secret_access_key, aws_region, bucket_name = prompt_for_aws_credentials()
        os.environ['AWS_ACCESS_KEY_ID'] = aws_access_key_id
        os.environ['AWS_SECRET_ACCESS_KEY'] = aws_secret_access_key
        os.environ['AWS_REGION'] = aws_region
        os.environ['BUCKET_NAME'] = bucket_name

    load_data(
        target=config_data['load']['target'],
        config=get_env_variables(config_data['load']['config']),
        data=pd.read_json(StringIO(transformed_data_json), orient='split')
    )

    typer.echo("ETL pipeline completed successfully.")


if __name__ == "__main__":
    app()
