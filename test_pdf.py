import os

import PyPDF2
import pytest

from navigation import paths_keeper
from pyfiles.text_similarity import TextSimilarly


def recursive_container_compare(val_1, val_2):
    assert isinstance(val_1, type(val_2))
    if isinstance(val_1, (list, tuple)):
        assert len(val_1) == len(val_2)
        for elem_1, elem_2 in zip(val_1, val_2):
            recursive_container_compare(elem_1, elem_2)
    elif isinstance(val_1, dict):
        assert set(val_1) == set(val_2)
        for key in val_1:
            recursive_container_compare(val_1[key], val_2[key])
    elif isinstance(val_1, str):
        assert val_1 == val_2



@pytest.mark.parametrize(
    "test_path",
    paths_keeper.get_paths("pdf"),
    ids=paths_keeper.get_ids("pdf"),
)
def test_pdf_text(test_path):
    baseline_path = os.path.join(test_path, "baseline.pdf")
    subject_path = os.path.join(test_path, "subject.pdf")

    baseline_pdf = PyPDF2.PdfFileReader(baseline_path)
    baseline_text = "".join(page.extract_text() for page in baseline_pdf.pages)

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
    subject_path = os.path.join(test_path, "subject.pdf")

    baseline_pdf = PyPDF2.PdfFileReader(baseline_path)
    baseline_format = [page["/Resources"] for page in baseline_pdf.pages]

    subject_pdf = PyPDF2.PdfFileReader(subject_path)
    subject_format = [page["/Resources"] for page in subject_pdf.pages]

    recursive_container_compare(baseline_format, subject_format)
