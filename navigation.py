import json
import os
from typing import Iterable


class PathsKeeper:
    def __init__(self, config_path: str = "config.json"):
        with open(config_path, encoding="utf-8") as config_file:
            self._source = json.load(config_file)

    def _file_paths(self, section: str, case_type: str):
        path = os.path.join(self._source[section], case_type)
        return (os.path.join(path, file_name) for file_name in os.listdir(path))

    def get_paths(self, section: str) -> Iterable[str]:
        if section not in self._source:
            return []

        return (
            os.path.join(self._source[section], name)
            for name in os.listdir(self._source[section])
        )

    def get_ids(self, section: str) -> Iterable[str]:
        if section not in self._source:
            return []

        return (os.path.basename(entry) for entry in os.listdir(self._source[section]))


paths_keeper = PathsKeeper()
