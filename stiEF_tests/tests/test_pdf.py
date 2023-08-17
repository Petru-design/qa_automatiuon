import os

import PyPDF2

from stiEF_tests.tests.utils.comparators import recursive_container_compare, compare_texts


def test_pdf_text(reference_path, subject_path, result_path, naming_prefix):
    baseline_pdf = PyPDF2.PdfFileReader(reference_path)
    subject_pdf = PyPDF2.PdfFileReader(subject_path)

    compare_texts(
        "".join(page.extract_text() for page in baseline_pdf.pages),
        "".join(page.extract_text() for page in subject_pdf.pages),
        os.path.join(result_path, "text_result.txt"),
    )


def test_pdf_format(reference_path, subject_path, result_path, naming_prefix):
    baseline_pdf = PyPDF2.PdfFileReader(reference_path)
    subject_pdf = PyPDF2.PdfFileReader(subject_path)

    baseline_format = [page["/Resources"] for page in baseline_pdf.pages]
    subject_format = [page["/Resources"] for page in subject_pdf.pages]

    recursive_container_compare(baseline_format, subject_format)
