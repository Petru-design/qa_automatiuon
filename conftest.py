import json
import os


class ArgumentError(Exception):
    pass


_expansions = {
    "test_docx.py": {
        "test_text": "docx",
        "test_format": "docx",
    },
    "test_images.py": {"test_jpg": "jpg", "test_png": "png"},
    "test_pdf.py": {
        "test_text": "pdf",
        "test_format": "pdf",
    },
    "test_pptx.py": {
        "test_text": "pptx",
    },
    "test_xlsx.py": {
        "test_text": "xlsx",
        "test_format": "xlsx",
    },
}


def pytest_addoption(parser):
    parser.addoption("--scenario_name", action="store")
    parser.addoption("--scenario_path", action="store")
    parser.addoption("--baseline_path", action="store")
    parser.addoption("--result_path", action="store")


def pytest_generate_tests(metafunc):
    params = {
        "scenario_name": metafunc.config.getoption("scenario_name"),
        "scenario_path": metafunc.config.getoption("scenario_path"),
        "baseline_path": metafunc.config.getoption("baseline_path"),
        "result_path": metafunc.config.getoption("result_path"),
    }

    if all(param is None for param in params.values()):
        config_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "config.json"
        )
        with open(config_path, encoding="utf-8") as config_file:
            config = json.load(config_file)
        paths = {}
        ids = {}
        for values in config:
            paths.setdefault(values["expansion"], []).append(
                (
                    values["base"],
                    values["subject"],
                    values["results"],
                )
            )
            ids.setdefault(values["expansion"], []).append(values["name"])
        expansion = _expansions[metafunc.definition.parent.name][
            metafunc.definition.name
        ]
        metafunc.parametrize(
            "baseline_path,subject_path,result_path",
            paths[expansion],
            ids=ids[expansion],
        )

    elif any(param is None for param in params):
        raise ArgumentError(f"Some params are set, while others are not: {params}")

    else:
        metafunc.parametrize(
            "baseline_path,subject_path,result_path",
            [[params["scenario_path"], params["baseline_path"], params["result_path"]]], 
            ids = [params["scenario_name"]],
        )
