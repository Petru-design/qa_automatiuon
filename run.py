import argparse
import json
import os

import pytest


repo = os.path.dirname(os.path.realpath(__file__))

test_names = {
    "docx": {
        "text": os.path.join(repo, "test_docx.py") + "::test_text",
        "format": os.path.join(repo, "test_docx.py") + "::test_format",
    },
    "jpg": {
        "image": os.path.join(repo, "test_images.py") + "::test_jpg",
    },
    "png": {
        "image": os.path.join(repo, "test_images.py") + "::test_png",
    },
    "pdf": {
        "text": os.path.join(repo, "test_pdf.py") + "::test_pdf_text",
        "format": os.path.join(repo, "test_pdf.py") + "::test_pdf_format",
    },
    "pptx": {
        "text": os.path.join(repo, "test_pptx.py") + "::test_pptx_test",
    },
    "xlsx": {
        "text": os.path.join(repo, "test_xlsx.py") + "::test_xlsx_text",
        "format": os.path.join(repo, "test_xlsx.py") + "::test_xlsx_format",
    },
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("scenario_name", help="Name of scenario.")
    parser.add_argument("scenario_path", help="Path of scenario.")
    parser.add_argument("baseline_path", help="Path to actual baseline cases.")
    parser.add_argument("result_path", help="Where to store results.")
    parser.add_argument(
        "expansion",
        help="""
        Expansion of exported scenario file.
        """,
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

    config_path = os.path.join(repo, "config.json")
    with open(config_path, "w", encoding="utf-8") as config:
        json.dump(
            [
                {
                    "name": args.scenario_name,
                    "base": args.baseline_path,
                    "subject": args.scenario_path,
                    "results": args.result_path,
                    "expansion": args.expansion,
                }
            ],
            config,
        )

    test_args = [f"{test_names[args.expansion][args.test]}[{args.scenario_name}]"]
    if args.xml:
        test_args.extend(("--junitxml", os.path.join(args.result_path, "result.xml")))
    if args.csv:
        test_args.extend(
            (
                "--csv",
                os.path.join(args.result_path, "result.csv"),
            )
        )
    retcode = pytest.main(test_args)
