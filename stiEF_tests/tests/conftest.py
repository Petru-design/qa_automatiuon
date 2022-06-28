import json


class NoConfigError(Exception):
    pass


class ArgumentError(Exception):
    pass


_test_names = {
    ("stiEF_tests/tests/test_docx.py", "test_docx_text"): "test_docx_text",
    ("stiEF_tests/tests/test_docx.py", "test_docx_format"): "test_docx_format",
    ("stiEF_tests/tests/test_images.py", "test_jpg"): "test_jpg",
    ("stiEF_tests/tests/test_images.py", "test_png"): "test_png",
    ("stiEF_tests/tests/test_pdf.py", "test_pdf_text"): "test_pdf_text",
    ("stiEF_tests/tests/test_pdf.py", "test_pdf_format"): "test_pdf_format",
    ("stiEF_tests/tests/test_pptx.py", "test_pptx_text"): "test_pptx_text",
    ("stiEF_tests/tests/test_xlsx.py", "test_xlsx_text"): "test_xlsx_text",
    ("stiEF_tests/tests/test_xlsx.py", "test_xlsx_format"): "test_xlsx_format",
}


# def pytest_addoption(parser):
#     parser.addoption("--scenario_name", action="store")
#     parser.addoption("--scenario_path", action="store")
#     parser.addoption("--baseline_path", action="store")
#     parser.addoption("--result_path", action="store")
#     parser.addoption("--config_path", action="store", default="../config.json")


def pytest_generate_tests(metafunc):
    params = {
        "scenario_name": metafunc.config.getoption("scenario_name"),
        "scenario_path": metafunc.config.getoption("scenario_path"),
        "baseline_path": metafunc.config.getoption("baseline_path"),
        "result_path": metafunc.config.getoption("result_path"),
    }
    config_path = metafunc.config.getoption("config_path")

    if all(param is None for param in params.values()):
        if not config_path:
            raise NoConfigError("At least, provide the path to the config file.")

        with open(config_path, encoding="utf-8") as config_file:
            config = json.load(config_file)
        paths = {}
        ids = {}
        for values in config:
            paths.setdefault(values["test"], []).append(
                (
                    values["base"],
                    values["subject"],
                    values["results"],
                )
            )
            ids.setdefault(values["test"], []).append(values["name"])
        test_name = _test_names[(metafunc.definition.parent.name, metafunc.definition.name)]
        metafunc.parametrize(
            "baseline_path,subject_path,result_path",
            paths[test_name],
            ids=ids[test_name],
        )

    elif any(param is None for param in params):
        raise ArgumentError(f"Some params are set, while others are not: {params}")

    else:
        metafunc.parametrize(
            "baseline_path,subject_path,result_path",
            [[params["scenario_path"], params["baseline_path"], params["result_path"]]],
            ids=[params["scenario_name"]],
        )