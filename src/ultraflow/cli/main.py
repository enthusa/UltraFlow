import typer
from ultraflow import Flow, __version__

app = typer.Typer(
    name='uf',
    help='UltraFlow 命令行工具',
    add_completion=False
)


@app.command()
def greet(name: str = typer.Argument(..., help='要问候的名字')):
    flow = Flow()
    typer.echo(flow(name=name))


@app.command()
def version():
    typer.echo(__version__)
