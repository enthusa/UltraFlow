import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Any


class FlowProcessor:
    def __init__(self, flow: str, data_path: str, max_workers: int = 2):
        self.flow = flow
        self.data_path = Path(data_path)
        self.max_workers = max_workers

    def _load_and_validate(self) -> List[Any]:
        if not self.data_path.exists():
            raise FileNotFoundError(f"Error: {self.data_path} does not exist")
        with open(self.data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data if isinstance(data, list) else [data]

    def _process_item(self, flow: Any, item: dict) -> Any:
        input_signature = getattr(flow, '_inputs', {})
        if not input_signature:
            return flow(**item)
        resolved_inputs = {name: item.get(name) for name in input_signature}
        return flow(**resolved_inputs)

    def _run_single_thread(self, flow: Any, items: List[Any]) -> List[Any]:
        print("Single-thread processing mode")
        return [self._process_item(flow, item) for item in items]

    def _run_multi_thread(self, flow: Any, items: List[Any]) -> List[Any]:
        print(f"Multi-thread processing mode, using {self.max_workers} workers")
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self._process_item, flow, item): item for item in items}
            return [future.result() for future in as_completed(futures)]

    def run(self) -> List[Any]:
        items = self._load_and_validate()
        if self.max_workers < 2:
            return self._run_single_thread(self.flow, items)
        else:
            return self._run_multi_thread(self.flow, items)
