import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from ultraflow.core.flow import Prompty


class FlowProcessor:
    def __init__(self, flow: Prompty, data_path: str, max_workers: int = 2):
        self.flow = flow
        self.data_path = Path(data_path)
        self.max_workers = max_workers

    def _load_and_validate(self) -> list[Any]:
        if not self.data_path.exists():
            raise FileNotFoundError(f'Error: {self.data_path} does not exist')
        with open(self.data_path, encoding='utf-8') as f:
            data = json.load(f)
        return data if isinstance(data, list) else [data]

    @staticmethod
    def _process_item(flow: Prompty, item: dict) -> Any:
        resolved_inputs = flow.resolve_inputs(item)
        return flow(**resolved_inputs)

    def _run_single_thread(self, flow: Prompty, items: list[Any]) -> list[Any]:
        print('Single-thread processing mode')
        return [self._process_item(flow, item) for item in items]

    def _run_multi_thread(self, flow: Prompty, items: list[Any]) -> list[Any]:
        print(f'Multi-thread processing mode, using {self.max_workers} workers')
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self._process_item, flow, item): item for item in items}
            return [future.result() for future in as_completed(futures)]

    def run(self) -> list[Any]:
        items = self._load_and_validate()
        if self.max_workers < 2:
            return self._run_single_thread(self.flow, items)
        else:
            return self._run_multi_thread(self.flow, items)
