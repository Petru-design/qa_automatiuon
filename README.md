# QA Automatization tool

A set of tools to test stiEF scenarios. Main application of QAATool is a regression testing. It takes number of stiEF scenarios and compares it agains their previous versions.
There are multiple way to run tests with QAATool.
## With config.
QAATool can read json config with test data location to run tests.
1. Create json file with data.
2. Run pytest in root folder of project. You may run it with `--config_path` parameter to point to your config. By default, QAATool will look for `config.json` in it's root folder.

Config format example:
```json
[
    {
        "name": "Scenario name 1",
        "base": "path\\to\\reference\\image",
        "subject": "path\\to\\test\\subject",
        "results": "path\\to\\where\\results\\should\\be\\stored",
        "test": "test_type"
    },
    {
        "name": "Scenario name 2",
        "base": "path\\to\\reference\\image",
        "subject": "path\\to\\test\\subject",
        "results": "path\\to\\where\\results\\should\\be\\stored",
        "test": "test_type"
    }
]
```
QAATool has 9 types of test. Below is a list of them, with corresponding `pytest`-format names:

    test_docx_text      stiEF_tests/tests/test_docx.py::test_docx_text
    test_docx_format    stiEF_tests/tests/test_docx.py::test_docx_format
    test_jpg            stiEF_tests/tests/test_images.py::test_jpg
    test_png            stiEF_tests/tests/test_images.py::test_png
    test_pdf_text       stiEF_tests/tests/test_pdf.py::test_pdf_text
    test_pdf_format     stiEF_tests/tests/test_pdf.py::test_pdf_format
    test_pptx_text      stiEF_tests/tests/test_pptx.py::test_pptx_text
    test_xlsx_text      stiEF_tests/tests/test_xlsx.py::test_xlsx_text
    test_xlsx_format    stiEF_tests/tests/test_xlsx.py::test_xlsx_format

## With parameters.
QAATool may run without any config, in case if all the necessary data is provided with parameters. It's the same data, that is provided with config file:

`--name` - name of scenario.

`--subject` - path to test subject

`--reference` - path to reference image

`--results` - path to location to store results in

To run the specific test, user should...well, specify the test, using a standart pytest format. E.g. to test docx format, use `stiEF_tests/tests/test_docx.py::test_docx_format` as an argument.

## As python package
Now some magic. To build QAATool into python package you'd need `build` package installed. Then just run `python -m build` in root folder. After QAATool is build, you can find it's tar in `dist` folder. You can install it into your environment with `pip install...`. Than run `python -m stiEF_tests`. If you want to run tests against config file, just as with running from root - use default config name or `--config_path` parameter. If you want to run your own test - use the same parameters. Only difference is that package does not understand standart pytest naming notation. Instead use `--test` parameter with value just like in config file.

## As executable
To build QAA executable, use the python package called `pyinstaller`. Run `pyinstaller .\run_stiEF_test.py --clean --collect-all stiEF_tests --noconfirm` to build executable. Resulted programm would be able to run only on the system of the same type it was build on. Built executable is stored in `dist\run_stiEF_tests` as `run_stiEF_tests.exe`. It can be run with all the same arguments, as python script or module.

## Side note
Pytest, apperantly, has a bug, that does not allow it to run with arguments. So yeah, we're using a workaround here, and instead of running `pytest -yargs stiEF_tests` as any sane person would, we are executing code in `__main__.py` module, like some madmen.