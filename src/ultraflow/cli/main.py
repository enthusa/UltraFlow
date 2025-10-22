import time
from pathlib import Path

import click
from promptflow.tracing import start_trace

from ultraflow import FlowProcessor, Prompty, __version__, generate_connection_config, generate_example_prompty


@click.group()
@click.version_option(version=__version__, help='显示 UltraFlow CLI 工具的版本号')
def app():
    """UltraFlow CLI - 强大的基于 Prompty 的提示词工程开发、测试、部署一站式工具。"""
    pass


@app.command(help='初始化 UltraFlow 项目，生成连接配置文件')
@click.argument('project_name', required=False)
def init(project_name):
    project_path = Path(project_name) if project_name else Path.cwd()
    config_file = project_path / '.ultraflow' / 'connection_config.json'
    if config_file.exists() and config_file.is_file():
        click.echo(f'⚠️ 连接配置文件已存在: {config_file.resolve()}')
        return
    config_file.parent.mkdir(parents=True, exist_ok=True)
    config_file.write_text(generate_connection_config(), encoding='utf-8')
    click.echo(f'✅ 成功生成连接配置文件: {config_file}')
    click.echo('\n📝 下一步:')
    click.echo(f'1. 进入项目目录 {project_path}，编辑配置文件，设置 API Key: {config_file}')
    click.echo('2. 使用 "uf new <flow_name>" 创建新的流程模板')
    click.echo('3. 使用 "uf run <flow_name>" 运行流程')


@app.command(help='创建新的流程模板（包括 .prompty 和 .json 文件）')
@click.argument('flow_name')
def new(flow_name):
    flow_path = Path(flow_name)
    flow_stem = flow_path.stem
    flow_dir = flow_path.parent
    flow_file = flow_dir / f'{flow_stem}.prompty'
    data_file = flow_dir / f'{flow_stem}.json'
    if flow_file.exists() or data_file.exists():
        if flow_file.exists():
            click.echo(f'⚠️ 文件已存在: {flow_file.resolve()}')
        if data_file.exists():
            click.echo(f'⚠️ 文件已存在: {data_file.resolve()}')
        return

    data, prompt = generate_example_prompty()
    data_file.parent.mkdir(parents=True, exist_ok=True)
    data_file.write_text(data, encoding='utf-8')
    flow_file.write_text(prompt, encoding='utf-8')
    click.echo('✅ 成功创建流程模板:')
    click.echo(f'1. Prompt 文件: {flow_file}')
    click.echo(f'2. 数据文件:    {data_file}')
    click.echo('\n📝 下一步:')
    click.echo(f'1. 编辑 {flow_file} 定义你的提示词')
    click.echo(f'2. 编辑 {data_file} 准备测试数据')
    click.echo(f'3. 运行流程: uf run {flow_name}')


@app.command(help='运行指定的流程，使用输入数据进行批量测试')
@click.argument('flow_name')
@click.option('--data', '-d', help='输入数据文件路径（JSON 格式）。如不指定，自动查找同名 .json 文件')
@click.option(
    '--max_workers', '-w', type=int, default=2, show_default=True, help='最大并发线程数。设为 1 使用单线程模式'
)
def run(flow_name, data, max_workers):
    flow_path = Path(flow_name)
    flow_stem = flow_path.stem
    flow_dir = flow_path.parent
    flow_file = flow_dir / f'{flow_stem}.prompty'
    data_file = Path(data) if data else flow_dir / f'{flow_stem}.json'
    flow = Prompty.load(flow_file)
    collection = f'{flow_stem}_{flow.model}_{time.strftime("%Y%m%d%H%M%S", time.localtime())}'
    start_trace(collection=collection)
    processor = FlowProcessor(flow=flow, data_path=data_file, max_workers=max_workers)
    click.echo(f'🚀 执行任务 {flow_file}，数据 {data_file}')
    processor.run()
    click.echo('✅ 流程执行完成')


if __name__ == '__main__':
    app()
