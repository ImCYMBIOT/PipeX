import typer
import yaml

from app.load import load_data
from app.extract import extract_data
from app.transform import transform_data

app = typer.Typer()

@app.command()
def extract(source: str, config: str):
    typer.echo(f"Extracting data from {source} using config: {config}")
    with open(config, 'r') as file:
        config_data = yaml.safe_load(file)
    
    data = extract_data(
        source_type=source,
        connection_details=config_data['connection_details'],
        query_or_endpoint=config_data['query_or_endpoint']
    )
    typer.echo("Data extraction complete.")
    return data

@app.command()
def transform(script: str, config: str):
    typer.echo(f"Transforming data using script: {script} and config: {config}")
    transform_data(script, config)
    typer.echo("Data transformation complete.")

@app.command()
def load(target: str, config: str):
    typer.echo(f"Loading data to {target} using config: {config}")
    load_data(target, config)
    typer.echo("Data loading complete.")

@app.command()
def run(config: str = "config.yaml"):
    typer.echo(f"Running ETL pipeline with config: {config}")
    with open(config, 'r') as file:
        config_data = yaml.safe_load(file)
    
    # Extract
    typer.echo("Extracting data...")
    extract_data(
        source_type=config_data['extract']['source'],
        connection_details=config_data['extract']['connection_details'],
        query_or_endpoint=config_data['extract']['query_or_endpoint']
    )
    
    # Transform
    typer.echo("Transforming data...")
    transform_data(
        script=config_data['transform']['script'],
        config=config_data['transform']['config']
    )
    
    # Load
    typer.echo("Loading data...")
    load_data(
        target=config_data['load']['target'],
        config=config_data['load']['config']
    )

if __name__ == "__main__":
    app()