import os

import PyPDF2
import pytest

from utils.navigation import paths_keeper
from utils.comparators import recursive_container_compare, compare_texts


@pytest.mark.parametrize(
    "test_path",
    paths_keeper.get_paths("pdf"),
    ids=paths_keeper.get_ids("pdf"),
)
def test_pdf_text(test_path):
    baseline_pdf = PyPDF2.PdfFileReader(os.path.join(test_path, "baseline.pdf"))
    subject_pdf = PyPDF2.PdfFileReader(os.path.join(test_path, "subject.pdf"))

    compare_texts(
        "".join(page.extract_text() for page in baseline_pdf.pages),
        "".join(page.extract_text() for page in subject_pdf.pages),
        os.path.join(test_path, "text_result.txt"),
    )


@pytest.mark.parametrize(
    "test_path",
    paths_keeper.get_paths("pdf"),
    ids=paths_keeper.get_ids("pdf"),
)
def test_pdf_format(test_path):
    baseline_pdf = PyPDF2.PdfFileReader(os.path.join(test_path, "baseline.pdf"))
    subject_pdf = PyPDF2.PdfFileReader(os.path.join(test_path, "subject.pdf"))

    baseline_format = [page["/Resources"] for page in baseline_pdf.pages]
    subject_format = [page["/Resources"] for page in subject_pdf.pages]

    recursive_container_compare(baseline_format, subject_format)
