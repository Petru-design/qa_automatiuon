import json
import os


class PathsKeeper:
    def __init__(self, config_path: str = "config.json"):
        with open(config_path, encoding="utf-8") as config_file:
            self._config = json.load(config_file)

        self._ids: dict[str, list[str]] = {}
        self._paths: dict[str, list[tuple]] = {}
        for values in self._config:
            self._ids.setdefault(values["expansion"], []).append(values["name"])
            self._paths.setdefault(values["expansion"], []).append(
                (
                    values["base"],
                    values["subject"],
                    values["results"],
                )
            )

    def get_paths(self, section: str) -> list:
        return self._paths.get(section, [])

    def get_ids(self, section: str) -> list[str]:
        return self._ids.get(section, [])


_config_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "config.json"
)
paths_keeper = PathsKeeper(_config_path)
