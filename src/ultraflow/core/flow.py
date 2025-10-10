import json
import logging
import re
from os import PathLike
from pathlib import Path
from typing import Optional, Union

import json_repair
import requests
from promptflow._utils.yaml_utils import load_yaml_string
from promptflow.core._prompty_utils import convert_prompt_template
from promptflow.tracing import trace
from promptflow.tracing._experimental import enrich_prompt_template
from promptflow.tracing._trace import TraceType, _traced

from ultraflow.core.utils import find_connection_config


class Prompty:
    def __init__(self, path: Union[str, PathLike], model: Optional[dict] = None, **kwargs):
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
        url = self.connection['url']
        api_key = self.connection['api_key']
        api_key_tail = api_key[-4:]
        traced_call_chat_api = _traced(func=self.call_chat_api, args_to_ignore=['api_key'], name='call_chat_api')
        response = traced_call_chat_api(data, url, api_key, api_key_tail)
        traced_chat = _traced(func=self.chat, trace_type=TraceType.LLM, args_to_ignore=['response'], name='chat')
        traced_chat(data['messages'], response)

        is_json = 'response_format' in data and data['response_format']['type'] == 'json_object'
        if 'choices' in response:
            reply = response['choices'][0]['message']['content']
            if is_json:
                return json_repair.loads(reply)
            return reply

    def call_chat_api(self, data, url, api_key, api_key_tail):
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {api_key}'}
        r = requests.post(url, json=data, headers=headers)
        return r.json()

    @staticmethod
    def chat(messages, response):
        return response

    @classmethod
    def load(cls, source: Union[str, PathLike], **kwargs):
        source_path = Path(source)
        return cls._load(path=source_path, **kwargs)

    @classmethod
    def _load(cls, path: Path, **kwargs):
        return cls(path=path, **kwargs)

    @classmethod
    def _select_connection_by_model(cls, model_name):
        connection_config_file = find_connection_config()
        if connection_config_file is None:
            raise FileNotFoundError('Connection config file not found.')
        logging.info('Load connection from %s', connection_config_file)
        with open(connection_config_file, encoding='utf-8') as file:
            connection_config = json.load(file)
        for _, connection in connection_config.items():
            model_list = connection.get('model_list', [])
            if model_name in model_list:
                return connection
        raise ValueError(f'Model {model_name} not found in any connection in connection_config.json')

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
