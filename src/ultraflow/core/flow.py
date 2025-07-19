from __future__ import annotations

import json
import re
from os import PathLike
from os import path as osp
from pathlib import Path

import json_repair
import requests
from promptflow._utils.yaml_utils import load_yaml_string
from promptflow.core._prompty_utils import convert_prompt_template
from promptflow.tracing import trace
from promptflow.tracing._experimental import enrich_prompt_template
from promptflow.tracing._trace import _traced


class Prompty:
    def __init__(self, path: str | PathLike, model: dict | None = None, **kwargs):
        self.path = path
        configs, self._template = self._parse_prompty(path)
        self.parameters = {}
        if 'configuration' in configs['model']:
            self.parameters['model'] = configs['model']['configuration']['model']
        self.parameters.update(configs['model']['parameters'])
        if model:
            if 'configuration' in model:
                self.parameters['model'] = model['configuration'].model
            self.parameters.update(model['parameters'])
        self.model = self.parameters['model']
        self._inputs = configs.get('inputs', {})
        self.connection = self._select_connection_by_model(self.parameters['model'])

    @trace
    def __call__(self, *args, **kwargs):
        inputs = self.resolve_inputs(kwargs)
        enrich_prompt_template(self._template, variables=inputs)

        traced_convert_prompt_template = _traced(func=convert_prompt_template, args_to_ignore=['api'])
        messages = traced_convert_prompt_template(self._template, inputs, 'chat')

        data = {'messages': messages, **self.parameters}
        response = self.call_llm_api(data)
        is_json = 'response_format' in data and data['response_format']['type'] == 'json_object'
        if 'choices' in response:
            reply = response['choices'][0]['message']['content']
            if is_json:
                return json_repair.loads(reply)
            return reply

    @trace
    def call_llm_api(self, data):
        url = self.connection['url']
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.connection["api_key"]}'}
        r = requests.post(url, json=data, headers=headers)
        return r.json()

    @classmethod
    def load(cls, source: str | PathLike, **kwargs):
        source_path = Path(source)
        return cls._load(path=source_path, **kwargs)

    @classmethod
    def _load(cls, path: Path, **kwargs):
        return cls(path=path, **kwargs)

    @classmethod
    def _select_connection_by_model(cls, model_name):
        connection_config_file = osp.join(osp.expanduser('~'), '.ultraflow/connection_config.json')
        with open(connection_config_file, encoding='utf-8') as file:
            connection_config = json.load(file)
        for _, connection in connection_config.items():
            model_list = connection.get('model_list', [])
            if model_name in model_list:
                return connection
        raise ValueError(f'未在 connection_config.json 中找到包含模型 {model_name} 的 connection')

    @staticmethod
    def _parse_prompty(path):
        with open(path, encoding='utf-8') as f:
            prompty_content = f.read()
        pattern = r'-{3,}\n(.*?)-{3,}\n(.*)'
        result = re.search(pattern, prompty_content, re.DOTALL)
        config_content, prompt_template = result.groups()
        configs = load_yaml_string(config_content)
        return configs, prompt_template

    def resolve_inputs(self, input_values):
        resolved_inputs = {}
        for input_name, _value in self._inputs.items():
            resolved_inputs[input_name] = input_values[input_name]
        return resolved_inputs
