import os

import PyPDF2
import pytest

from navigation import paths_keeper
from pyfiles.text_similarity import TextSimilarly
from utils.comparators import recursive_container_compare


@pytest.mark.parametrize(
    "test_path",
    paths_keeper.get_paths("pdf"),
    ids=paths_keeper.get_ids("pdf"),
)
def test_pdf_text(test_path):
    baseline_path = os.path.join(test_path, "baseline.pdf")
    baseline_pdf = PyPDF2.PdfFileReader(baseline_path)
    baseline_text = "".join(page.extract_text() for page in baseline_pdf.pages)

    subject_path = os.path.join(test_path, "subject.pdf")
    subject_pdf = PyPDF2.PdfFileReader(subject_path)
    subject_text = "".join(page.extract_text() for page in subject_pdf.pages)

    compare = TextSimilarly(baseline_text, subject_text)
    _, score = compare.damerau_levenshtein()
    assert score == 1


@pytest.mark.parametrize(
    "test_path",
    paths_keeper.get_paths("pdf"),
    ids=paths_keeper.get_ids("pdf")
)
def test_pdf_format(test_path):
    baseline_path = os.path.join(test_path, "baseline.pdf")
    baseline_pdf = PyPDF2.PdfFileReader(baseline_path)
    baseline_format = [page["/Resources"] for page in baseline_pdf.pages]

    subject_path = os.path.join(test_path, "subject.pdf")
    subject_pdf = PyPDF2.PdfFileReader(subject_path)
    subject_format = [page["/Resources"] for page in subject_pdf.pages]

    recursive_container_compare(baseline_format, subject_format)
