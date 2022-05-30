import json
import os


class PathsKeeper:
    def __init__(self, config_path: str = "config.json"):
        with open(config_path, encoding="utf-8") as config_file:
            self._config = json.load(config_file)

        self._ids: dict[str, list[str]] = {}
        self._paths: dict[str, list[str]] = {}
        for section, base_path in self._config.items():
            self._ids[section] = [os.path.basename(entry) for entry in os.listdir(base_path)]
            self._paths[section] = [os.path.join(base_path, name) for name in os.listdir(base_path)]

    def get_paths(self, section: str) -> list[str]:
        return self._paths.get(section, [])

    def get_ids(self, section: str) -> list[str]:
        return self._ids.get(section, [])


paths_keeper = PathsKeeper()
