import json
import os

import pytest


class ArgumentError(Exception):
    pass


@pytest.fixture(scope="session")
def params(pytestconfig):
    return [
        pytestconfig.getoption("scenario_path"),
        pytestconfig.getoption("baseline_path"),
        pytestconfig.getoption("result_path"),
    ]


@pytest.fixture
def paths(params, request):
    return request.param(params)


def get_paths(expansion):
    paths = {}
    path_i = 0

    def flow_control(params):
        if all(param is None for param in params):
            config_path = os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "config.json"
            )
            with open(config_path, encoding="utf-8") as config_file:
                config = json.load(config_file)

            for values in config:
                paths.setdefault(values["expansion"], []).append(
                    (
                        values["base"],
                        values["subject"],
                        values["results"],
                    )
                )
            return paths[expansion][0]

        if any(param is None for param in params):
            raise ArgumentError(
                f"Some params are set, while others are not: {params}"
            )

        return params

    def just_flow(_):
        nonlocal path_i
        path_i += 1
        return paths[expansion][path_i]

    yield flow_control

    if paths:
        for _ in range(len(paths) - 1):
            yield just_flow


@pytest.mark.parametrize("paths", get_paths("docx"), indirect=True)
def test_indirect(paths):
    print(paths)
