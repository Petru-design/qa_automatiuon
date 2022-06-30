import json


class NoConfigError(Exception):
    pass


class ArgumentError(Exception):
    pass


_test_names = {
    ("test_docx.py", "test_docx_text"): "test_docx_text",
    ("test_docx.py", "test_docx_format"): "test_docx_format",
    ("test_images.py", "test_jpg"): "test_jpg",
    ("test_images.py", "test_png"): "test_png",
    ("test_pdf.py", "test_pdf_text"): "test_pdf_text",
    ("test_pdf.py", "test_pdf_format"): "test_pdf_format",
    ("test_pptx.py", "test_pptx_text"): "test_pptx_text",
    ("test_xlsx.py", "test_xlsx_text"): "test_xlsx_text",
    ("test_xlsx.py", "test_xlsx_format"): "test_xlsx_format",
}


def pytest_generate_tests(metafunc):
    params = {
        "name": metafunc.config.getoption("name"),
        "subject": metafunc.config.getoption("subject"),
        "reference": metafunc.config.getoption("reference"),
        "results": metafunc.config.getoption("results"),
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
                    values["reference"],
                    values["subject"],
                    values["results"],
                )
            )
            ids.setdefault(values["test"], []).append(values["name"])
        test_name = _test_names[(metafunc.definition.parent.name, metafunc.definition.name)]
        metafunc.parametrize(
            "reference_path,subject_path,result_path",
            paths[test_name],
            ids=ids[test_name],
        )

    elif any(param is None for param in params):
        raise ArgumentError(f"Some params are set, while others are not: {params}")

    else:
        metafunc.parametrize(
            "reference_path,subject_path,result_path",
            [[params["reference"], params["subject"], params["results"]]],
            ids=[params["name"]],
        )
