import time

import click
from promptflow.tracing import start_trace

from ultraflow import FlowProcessor, Prompty, __version__


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
def version():
    click.echo(__version__)


if __name__ == '__main__':
    app()
