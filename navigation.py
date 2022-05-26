import json
import os
from typing import Iterable


class PathsKeeper:
    def __init__(self, config_path: str = "config.json"):
        with open(config_path, encoding="utf-8") as config_file:
            self._source = json.load(config_file)

    def _file_paths(self, section: str, case_type: str):
        return (
            os.path.join(self._source[section][case_type], file_name)
            for file_name in os.listdir(self._source[section][case_type])
        )

    def get_paths(self, section: str) -> Iterable[tuple[str, str]]:
        if section not in self._source:
            return []

        return zip(
            self._file_paths(section, "baseline"), self._file_paths(section, "subject")
        )

    def get_ids(self, section: str) -> Iterable[str]:
        if section not in self._source:
            return []

        return (
            os.path.basename(entry)
            for entry in os.listdir(self._source[section]["baseline"])
        )


paths_keeper = PathsKeeper()
