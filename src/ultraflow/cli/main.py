import time
from pathlib import Path

import click
from promptflow.tracing import start_trace

from ultraflow import FlowProcessor, Prompty, __version__, generate_connection_config, generate_example_prompty


@click.group()
@click.version_option(version=__version__, help='Show the version of UltraFlow CLI tool.')
def app():
    """UltraFlow CLI - A powerful workflow execution engine for Prompty-based flows."""
    pass


@app.command(help='Initialize an UltraFlow project by generating connection configuration.')
@click.argument('project_name', required=False)
def init(project_name):
    cwd = Path(project_name) if project_name else Path.cwd()
    config_file = cwd / '.ultraflow' / 'connection_config.json'
    if config_file.exists() and config_file.is_file():
        click.echo('⚠️ Connection config already exists.')
        return
    config_file.parent.mkdir(parents=True, exist_ok=True)
    config_file.write_text(generate_connection_config(), encoding='utf-8')
    click.echo(f'✅ Generated connection config at {config_file.resolve()}')


@app.command(help='Create a new example flow including .prompty and .json files.')
@click.argument('flow_name')
def new(flow_name):
    data, prompt = generate_example_prompty()
    cwd = Path.cwd()
    data_file = cwd / f'{flow_name}.json'
    prompt_file = cwd / f'{flow_name}.prompty'
    data_file.parent.mkdir(parents=True, exist_ok=True)
    data_file.write_text(data, encoding='utf-8')
    prompt_file.write_text(prompt, encoding='utf-8')
    click.echo(
        f'✅ Created example flow:\n'
        f'   📄 Prompt file: {prompt_file.resolve()}\n'
        f'   📦 Data file:   {data_file.resolve()}'
    )


@app.command(help='Run a specified flow with input data.')
@click.argument('flow_name')
@click.option('--data', help='Path to input data file in JSON format (optional if same-name .json exists).')
@click.option(
    '--max_workers',
    type=int,
    default=2,
    show_default=True,
    help='Maximum number of parallel workers to execute tasks concurrently.',
)
def run(flow_name, data, max_workers):
    flow_path = Path(flow_name)
    flow_stem = flow_path.stem
    flow_dir = flow_path.parent
    flow_file = flow_dir / f'{flow_stem}.prompty'
    data_file = flow_dir / f'{flow_stem}.json'
    flow = Prompty.load(flow_file)
    if data is None:
        data = data_file
    collection = f'{flow_stem}_{flow.model}_{time.strftime("%Y%m%d%H%M%S", time.localtime())}'
    start_trace(collection=collection)
    processor = FlowProcessor(flow=flow, data_path=data, max_workers=max_workers)
    click.echo(f"🚀 Running UltraFlow task from '{flow_file.resolve()}' using data '{data}'")
    processor.run()
    click.echo('✅ Flow execution completed successfully.')


if __name__ == '__main__':
    app()
