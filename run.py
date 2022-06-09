import argparse
import shutil

import pytest

from utils.move_files import move_files


test_names = {
    "docx": {
        "text": "./test_docx.py::test_text",
        "format": "./test_docx.py::test_format",
    },
    "jpg": {
        "image": "./test_image.py::test_jpg",
    },
    "png": {
        "image": "./test_image.py::test_png",
    },
    "pdf": {
        "text": "./test_pdf.py::test_pdf_text",
        "format": "./test_pdf.py::test_pdf_format",
    },
    "pptx": {
        "text": "./test_pptx.py::test_pptx_test",
    },
    "xlsx": {
        "text": "./test_xlsx.py::test_xlsx_text",
        "format": "./test_xlsx.py::test_xlsx_format",
    },
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("scenario_name", help="Name of scenario.")
    parser.add_argument("scenario_path", help="Path of scenario.")
    parser.add_argument("baseline_path", help="Path to actual baseline cases.")
    parser.add_argument(
        "expansion",
        help="""
        Expansion of exported scenario file.
        """
    )
    parser.add_argument(
        "test",
        help="""
        Test to run. Can be 'text', 'format' or 'image'. 
        """,
    )
    parser.add_argument(
        "--xml",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Store result in junit xml file.",
    )
    parser.add_argument(
        "--csv",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Store result in csv file.",
    )
    args = parser.parse_args()

    # fetch baseline from qa repo
    move_files([args.scenario_name], args.baseline_path, "./data", as_base=True)
    # fetch subject from export location
    move_files([args.scenario_name], args.scenario_path, "./data", as_subject=True)
    # choose tests to run

    test_args = [f"{test_names[args.expansion][args.test]}[{args.scenario_name}]"]

    # choose output
    if args.xml:
        test_args.extend(("--junitxml", "result.xml"))
    if args.csv:
        test_args.extend(
            (
                "--csv",
                "result.csv",
            )
        )
    retcode = pytest.main(test_args)
    # clean up
    shutil.rmtree("./data")
