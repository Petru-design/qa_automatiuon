import os

from pptx import Presentation
import pytest

from utils.navigation import paths_keeper
from pyfiles.text_similarity import TextSimilarly


def extract_text(prs):
    for slide in prs.slides:
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            for paragraph in shape.text_frame.paragraphs:
                for run in paragraph.runs:
                    yield run.text


@pytest.mark.parametrize(
    "test_path",
    paths_keeper.get_paths("pptx"),
    ids=paths_keeper.get_ids("pptx")
)
def test_pptx_text(test_path):
    baseline_path = os.path.join(test_path, "baseline.pptx")
    baseline_presentation = Presentation(baseline_path)
    baseline_text = "\n".join(extract_text(baseline_presentation))
    
    subject_path = os.path.join(test_path, "subject.pptx")
    subject_presentation = Presentation(subject_path)
    subject_text = "\n".join(extract_text(subject_presentation))

    compare = TextSimilarly(baseline_text, subject_text)
    _, score = compare.damerau_levenshtein()
    assert score == 1
