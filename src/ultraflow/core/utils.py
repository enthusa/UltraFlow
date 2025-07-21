from pathlib import Path
from typing import Optional


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
