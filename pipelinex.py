import typer
import os
import yaml
from app.cli import extract_data, transform_data, load_data, prompt_for_extraction_method, prompt_for_loading_method, prompt_for_aws_credentials
import pandas as pd
from io import StringIO
import questionary
import subprocess
import pyfiglet
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Main Typer application
app = typer.Typer()

def apply_env_variables(config):
    """
    Recursively replace placeholders in the config with environment variables.
    """
    if isinstance(config, dict):
        return {key: apply_env_variables(value) for key, value in config.items()}
    elif isinstance(config, str) and config.startswith("${") and config.endswith("}"):
        env_var = config[2:-1]
        return os.getenv(env_var, config)  # Replace with env value or leave as is
    else:
        return config

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
    ascii_art = pyfiglet.figlet_format("PipelineX", font="graffiti")
    typer.echo(ascii_art)
    typer.echo("Welcome to PipelineX Interactive Mode!")

    # Check if .env file exists, if not create a default one
    env_path = ".env"
    if not os.path.exists(env_path):
        with open(env_path, "w") as file:
            default_env = """# .env

# AWS Credentials
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
AWS_REGION=your-region
BUCKET_NAME=your-bucket-name

# API Credentials
API_TOKEN=your-api-token
API_ENDPOINT=your-api-endpoint
"""
            file.write(default_env)

    # Open .env file in default editor
    typer.echo("Opening .env file for editing. Please fill in your credentials.")
    subprocess.call([os.getenv('EDITOR', 'notepad'), env_path])

    # Reload environment variables from .env file
    load_dotenv()

    # Prompt for extraction method
    extraction_method = prompt_for_extraction_method()
    typer.echo(f"Selected extraction method: {extraction_method}")

    # Ask for configuration method
    config_method = questionary.select(
        "How would you like to provide extraction details?",
        choices=["Detail by config.yaml", "Detail through command line"]
    ).ask()

    if not config_method:
        typer.echo("No configuration method selected. Exiting.")
        raise typer.Exit()

    # Handle YAML-based configuration
    if config_method == "Detail by config.yaml":
        config_path = "app/config.yaml"

        # Create default config.yaml if it doesn't exist
        if not os.path.exists(config_path):
            with open(config_path, "w") as file:
                default_config = {
                    "extract": {
                        "source": extraction_method.lower(),
                        "connection_details": {"headers": {}},
                        "query_or_endpoint": "<your-endpoint-or-query>"
                    },
                    "transform": {
                        "script": "tests/transform_script.py",
                        "config": {
                            "drop_columns": ["id"],
                            "rename_columns": {"title": "post_title"},
                            "filter_rows": "post_title != ''",
                            "add_columns": {"new_column": "data['post_title'].str.len()"}
                        }
                    },
                    "load": {
                        "target": "S3 Bucket",
                        "config": {
                            "aws_access_key_id": "${AWS_ACCESS_KEY_ID}",
                            "aws_secret_access_key": "${AWS_SECRET_ACCESS_KEY}",
                            "region_name": "${AWS_REGION}",
                            "bucket_name": "${BUCKET_NAME}",
                            "file_name": "data.csv"
                        }
                    }
                }
                yaml.dump(default_config, file)

        # Open config.yaml in default editor
        typer.echo("Opening config.yaml for editing. Please fill in the details.")
        subprocess.call([os.getenv('EDITOR', 'notepad'), config_path])

        # Load and validate config.yaml
        with open(config_path, 'r') as file:
            config_data = yaml.safe_load(file)

        typer.echo("Config file loaded successfully.")

    else:
        # Command-line interactive input
        query_or_endpoint = typer.prompt("Enter the API endpoint or query")
        connection_details = {"headers": {}}

        loading_method = prompt_for_loading_method()
        if loading_method == "S3 Bucket":
            aws_access_key_id, aws_secret_access_key, aws_region, bucket_name = prompt_for_aws_credentials()
            os.environ['AWS_ACCESS_KEY_ID'] = aws_access_key_id
            os.environ['AWS_SECRET_ACCESS_KEY'] = aws_secret_access_key
            os.environ['AWS_REGION'] = aws_region
            os.environ['BUCKET_NAME'] = bucket_name

        config_data = {
            "extract": {
                "source": extraction_method.lower(),
                "connection_details": connection_details,
                "query_or_endpoint": query_or_endpoint
            },
            "transform": {
                "script": "tests/transform_script.py",
                "config": {
                    "drop_columns": ["id"],
                    "rename_columns": {"title": "post_title"},
                    "filter_rows": "post_title != ''",
                    "add_columns": {"new_column": "data['post_title'].str.len()"}
                }
            },
            "load": {
                "target": loading_method.lower(),
                "config": {
                    "aws_access_key_id": os.getenv('AWS_ACCESS_KEY_ID'),
                    "aws_secret_access_key": os.getenv('AWS_SECRET_ACCESS_KEY'),
                    "region_name": os.getenv('AWS_REGION'),
                    "bucket_name": os.getenv('BUCKET_NAME'),
                    "file_name": "data.csv"
                }
            }
        }

    # Apply environment variables to config
    config_data = apply_env_variables(config_data)

    # Execute ETL pipeline
    typer.echo("Extracting data...")
    extracted_data = extract_data(
        source_type=config_data['extract']['source'],
        connection_details=config_data['extract']['connection_details'],
        query_or_endpoint=config_data['extract']['query_or_endpoint']
    )
    data_json = extracted_data.to_json(orient='split')

    typer.echo("Transforming data...")
    transform_script = config_data['transform']['script']
    if not os.path.exists(transform_script):
        typer.echo(f"Transformation script not found: {transform_script}")
        raise typer.Exit()

    transformed_data = transform_data(
        script_path=transform_script,
        config=config_data['transform']['config'],
        data=pd.read_json(StringIO(data_json), orient='split')
    )
    transformed_data_json = transformed_data.to_json(orient='split')

    typer.echo("Loading data...")
    load_data(
        target=config_data['load']['target'],
        config=config_data['load']['config'],
        data=pd.read_json(StringIO(transformed_data_json), orient='split')
    )

    typer.echo("ETL pipeline completed successfully.")

if __name__ == "__main__":
    app(prog_name="pipelinex")