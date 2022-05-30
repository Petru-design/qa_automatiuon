import os

import PyPDF2
import pytest

from navigation import paths_keeper
from pyfiles.text_similarity import TextSimilarly


@pytest.mark.parametrize(
    "test_path",
    paths_keeper.get_paths("pdf"),
    ids=paths_keeper.get_ids("pdf"),
)
def test_pdf_text(test_path):
    baseline_path = os.path.join(test_path, "baseline.pdf")
    subject_path = os.path.join(test_path, "subject.pdf")

    with open(baseline_path, "rb") as baseline_file:
        pdfReader = PyPDF2.PdfFileReader(baseline_file)
        baseline_text = "".join(
            pdfReader.getPage(i).extractText() for i in range(pdfReader.numPages)
        )

    with open(subject_path, "rb") as subject_file:
        pdfReader = PyPDF2.PdfFileReader(subject_file)
        subject_text = "".join(
            pdfReader.getPage(i).extractText() for i in range(pdfReader.numPages)
        )

    compare = TextSimilarly(baseline_text, subject_text)
    _, score = compare.damerau_levenshtein()
    assert score == 1
