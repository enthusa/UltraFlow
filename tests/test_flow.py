from os import path as osp

import pandas as pd
from promptflow.tracing import start_trace

from ultraflow import Prompty


def test_chat():
    start_trace(collection='test_flow')
    dir_name = osp.dirname(__file__)
    flow = Prompty(f'{dir_name}/translate_english_chinese.prompty')
    df = pd.read_json(f'{dir_name}/translate_english_chinese.json')
    for row in df.itertuples():
        print(flow(text=row.text))
