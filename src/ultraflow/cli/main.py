import typer
from ultraflow.core.flow import Flow

app = typer.Typer(
    name='uf',
    help='UltraFlow 命令行工具'
)


@app.command()
def greet(name: str = typer.Argument(..., help='要问候的名字')):
    flow = Flow()
    typer.echo(flow(name=name))


@app.command()
def version():
    typer.echo('0.0.1')
