import typer

app = typer.Typer()  # Initialize the Typer application

@app.command()
def hello(name: str):
    typer.echo(f"Hello {name}!")
    
@app.command()
def lola(greet: str):
    typer.echo(f"bsdk,lehen ka boda {greet}!")

if __name__ == "__main__":  # Correct main block condition
    app()
