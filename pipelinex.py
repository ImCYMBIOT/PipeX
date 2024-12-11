import typer
import os
from app.cli import app as cli_app  

# Main Typer application
app = typer.Typer()

# Add the commands from the app.cli module as a subcommand group
app.add_typer(cli_app, name="app")


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
    extraction_method = typer.prompt("Select an extraction method (e.g., API, database)")
    typer.echo(f"Selected extraction method: {extraction_method}")

    # Prompt for loading method
    loading_method = typer.prompt("Select a loading method (e.g., S3 Bucket, local file)")
    typer.echo(f"Selected loading method: {loading_method}")

    # Prompt for AWS credentials if loading to S3
    if loading_method.lower() == "s3 bucket":
        aws_access_key_id = typer.prompt("Enter AWS Access Key ID")
        aws_secret_access_key = typer.prompt("Enter AWS Secret Access Key", hide_input=True)
        aws_region = typer.prompt("Enter AWS Region (e.g., ap-south-1)")
        bucket_name = typer.prompt("Enter S3 Bucket Name")
        os.environ['AWS_ACCESS_KEY_ID'] = aws_access_key_id
        os.environ['AWS_SECRET_ACCESS_KEY'] = aws_secret_access_key
        os.environ['AWS_REGION'] = aws_region
        os.environ['BUCKET_NAME'] = bucket_name

    # Run the ETL pipeline
    typer.echo("Starting the ETL pipeline...")
    cli_app.run()  # Ensure cli_app has a `run` command implemented


if __name__ == "__main__":
    app(prog_name="pipelinex")
