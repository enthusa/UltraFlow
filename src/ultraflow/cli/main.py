import time
from pathlib import Path

import click
from promptflow.tracing import start_trace

from ultraflow import FlowProcessor, Prompty, __version__, generate_connection_config, generate_example_prompty


@click.group()
def app():
    pass


@app.command()
@click.argument('flow_path')
@click.option('--data', help='Input data file path (JSON format)')
@click.option('--max_workers', type=int, default=2, help='Number of parallel workers, default is 2')
def run(flow_path, data, max_workers):
    flow = Prompty.load(flow_path)
    flow_name = flow_path.split('/')[-1].split('.')[0]
    collection = f'{flow_name}_{flow.model}_{time.strftime("%Y%m%d%H%M%S", time.localtime())}'
    start_trace(collection=collection)
    FlowProcessor(flow=flow, data_path=data, max_workers=max_workers).run()


@app.command()
def init():
    cwd = Path.cwd()
    config_file = cwd / '.ultraflow' / 'connection_config.json'
    if config_file.exists() and config_file.is_file():
        return
    config_file.parent.mkdir(parents=True, exist_ok=True)
    config_file.write_text(generate_connection_config(), encoding='utf-8')


@app.command()
@click.argument('flow_name')
def new(flow_name):
    cwd = Path.cwd()
    prompt_file = cwd / f'{flow_name}.prompty'
    prompt_file.parent.mkdir(parents=True, exist_ok=True)
    prompt_file.write_text(generate_example_prompty(), encoding='utf-8')


@app.command()
def version():
    click.echo(__version__)


if __name__ == '__main__':
    app()
