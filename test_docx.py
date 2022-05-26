import docx
import pytest

from navigation import paths_keeper
from pyfiles.compare import TextSimilarly


@pytest.mark.parametrize(
    "baseline_path, subject_path",
    paths_keeper.get_paths("docx"),
    ids=paths_keeper.get_ids("docx"),
)
def test_text(baseline_path, subject_path):
    baseline = docx.Document(baseline_path)
    subject = docx.Document(subject_path)

    compare = TextSimilarly(
        "\n".join(paragraph.text for paragraph in baseline.paragraphs),
        "\n".join(paragraph.text for paragraph in subject.paragraphs),
    )
    _, score = compare.damerau_levenshtein()
    assert score == 1


@pytest.mark.parametrize(
    "baseline_path, subject_path",
    paths_keeper.get_paths("docx"),
    ids=paths_keeper.get_ids("docx"),
)
def test_format(baseline_path, subject_path):
    baseline = docx.Document(baseline_path)
    subject = docx.Document(subject_path)

    compare_text(
        "\n".join(
            "".join(run.text for run in paragraph.runs)
            for paragraph in baseline.paragraphs
        ),
        "\n".join(
            "".join(run.text for run in paragraph.runs)
            for paragraph in subject.paragraphs
        ),
    )
