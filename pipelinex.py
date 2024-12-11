import typer
import os
import yaml
from app.cli import extract_data, transform_data, load_data, get_env_variables
from app.cli import prompt_for_extraction_method, prompt_for_loading_method, prompt_for_aws_credentials
import pandas as pd
from io import StringIO
# Main Typer application
app = typer.Typer()

@app.callback(invoke_without_command=True)
def welcome_message(ctx: typer.Context):
    """
    Default action when no command is provided.
    """
    if ctx.invoked_subcommand is None:
        typer.echo("Welcome to PipelineX!")
        typer.echo("Use the following commands to interact with PipelineX:")
        typer.echo("  pipelinex app <command>  - Access ETL subcommands.")
        typer.echo("  pipelinex run           - Run the ETL pipeline interactively.")
        typer.echo("  pipelinex --help        - Show help menu.")

@app.command()
def run():
    """
    Entry point for the PipelineX interactive ETL workflow.
    """
    typer.echo("Welcome to PipelineX Interactive Mode!")

    # Prompt for extraction method
    extraction_method = prompt_for_extraction_method()
    typer.echo(f"Selected extraction method: {extraction_method}")

    # Prompt for loading method
    loading_method = prompt_for_loading_method()
    typer.echo(f"Selected loading method: {loading_method}")

    # Prompt for AWS credentials if loading to S3
    if loading_method == "S3 Bucket":
        aws_access_key_id, aws_secret_access_key, aws_region, bucket_name = prompt_for_aws_credentials()
        os.environ['AWS_ACCESS_KEY_ID'] = aws_access_key_id
        os.environ['AWS_SECRET_ACCESS_KEY'] = aws_secret_access_key
        os.environ['AWS_REGION'] = aws_region
        os.environ['BUCKET_NAME'] = bucket_name

    # Load configuration
    config_path = "app/config.yaml"
    with open(config_path, 'r') as file:
        config_data = yaml.safe_load(file)

    # Extract data
    typer.echo("Extracting data...")
    query_or_endpoint = config_data['extract']['query_or_endpoint']
    connection_details = config_data['extract']['connection_details']
    extracted_data = extract_data(source_type=extraction_method, connection_details=connection_details, query_or_endpoint=query_or_endpoint)
    data_json = extracted_data.to_json(orient='split')

    # Transform data
    typer.echo("Transforming data...")
    transformed_data = transform_data(
        script_path=config_data['transform']['script'],  # Use `script_path`
        config=config_data['transform']['config'],
        data=pd.read_json(StringIO(data_json), orient='split')
    )

    transformed_data_json = transformed_data.to_json(orient='split')

    # Load data
    typer.echo("Loading data...")
    load_config = get_env_variables(config_data['load']['config'])
    load_data(target=loading_method, config=load_config, data=transformed_data)

    typer.echo("ETL pipeline completed successfully.")

if __name__ == "__main__":
    app(prog_name="pipelinex")