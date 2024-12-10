import typer
from app.cli import app as cli_app

app = typer.Typer()

# Add the commands from the app.cli module
app.add_typer(cli_app, name="app")

if __name__ == "__main__":
    app()