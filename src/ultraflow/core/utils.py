import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional


@dataclass
class Input:
    text: str


@dataclass
class Connection:
    url: str
    api_key: str
    model_list: list


def generate_connection_config():
    ark_connection = Connection(
        url='https://ark.cn-beijing.volces.com/api/v3/chat/completions',
        api_key='<your_key>',
        model_list=['doubao-1-5-pro-32k-250115', 'doubao-seed-1-6-thinking-250715'],
    )
    qwen_connection = Connection(
        url='https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',
        api_key='<your_key>',
        model_list=['qwen3-coder-plus'],
    )
    conns = {
        'ark_connection': asdict(ark_connection),
        'qwen_connection': asdict(qwen_connection),
    }
    return json.dumps(conns, indent=2, ensure_ascii=False)


def find_connection_config(start_path: Optional[Path] = None) -> Optional[Path]:
    if start_path is None:
        start_path = Path.cwd()
    current = start_path
    while current != current.parent:
        config_file = current / '.ultraflow' / 'connection_config.json'
        if config_file.exists() and config_file.is_file():
            return config_file
        current = current.parent
    config_file = Path.home() / '.ultraflow' / 'connection_config.json'
    if config_file.exists() and config_file.is_file():
        return config_file
    return None


def generate_example_prompty():
    i1 = Input(text='你要我做什么?')
    i2 = Input(text='写出你的测试用例')
    lst = [asdict(i1), asdict(i2)]
    data = json.dumps(lst, indent=2, ensure_ascii=False)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    example_prompt = os.path.join(script_dir, 'example.prompty')
    with open(example_prompt) as f:
        return data, f.read()
