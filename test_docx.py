import docx
import pytest

from navigation import paths_keeper
from pyfiles.text_similarity import TextSimilarly


font_comparable_fields = {
    "all_caps": type(None),
    "bold": bool,
    "color": {
        "rgb": type(None),
        "theme_color": type(None),
        "type": docx.enum.base.EnumValue,
    },
    "complex_script": type(None),
    "cs_bold": type(None),
    "cs_italic": type(None),
    "double_strike": type(None),
    "emboss": type(None),
    "hidden": type(None),
    "highlight_color": type(None),
    "imprint": type(None),
    "italic": type(None),
    "math": type(None),
    "name": type(None),
    "no_proof": type(None),
    "outline": type(None),
    "rtl": type(None),
    "shadow": type(None),
    "size": type(None),
    "small_caps": type(None),
    "snap_to_grid": type(None),
    "spec_vanish": type(None),
    "strike": type(None),
    "subscript": type(None),
    "superscript": type(None),
    "underline": type(None),
    "web_hidden": type(None),
}

paragraph_comparable_fields = {
    "alignment": type(None),
    "paragraph_format": {
        "alignment": type(None),
        "first_line_indent": type(None),
        "keep_together": type(None),
        "keep_with_next": type(None),
        "left_indent": type(None),
        "line_spacing": float,
        "line_spacing_rule": docx.enum.base.EnumValue,
        "page_break_before": bool,
        "right_indent": type(None),
        "space_after": docx.shared.Twips,
        "space_before": docx.shared.Twips,
    },
    "style": {
        "base_style": type(None),
        "builtin": bool,
        "font": font_comparable_fields,
        "hidden": bool,
        "locked": bool,
        "name": str,
        "paragraph_format": {
            "alignment": type(None),
            "first_line_indent": type(None),
            "keep_together": type(None),
            "keep_with_next": type(None),
            "left_indent": type(None),
            "line_spacing": docx.shared.Twips,
            "line_spacing_rule": docx.enum.base.EnumValue,
            "page_break_before": bool,
            "right_indent": type(None),
            "space_after": docx.shared.Twips,
            "space_before": docx.shared.Twips,
        },
        "priority": int,
        "quick_style": bool,
        "style_id": str,
        "type": docx.enum.base.EnumValue,
        "unhide_when_used": bool,
    },
}

run_comparable_fields = {
    "bold": bool,
    "font": font_comparable_fields,
    "italic": type(None),
    "style": {
        "base_style": type(None),
        "builtin": bool,
        "font": font_comparable_fields,
        "hidden": bool,
        "locked": bool,
        "name": str,
        "priority": int,
        "quick_style": bool,
        "style_id": str,
        "type": docx.enum.base.EnumValue,
        "unhide_when_used": bool,
    },
    "underline": type(None),
}


def recursive_compare(entity_1, entity_2, template: dict[str, None | dict | type]):
    for field_name, field_type in template.items():
        val_1 = getattr(entity_1, field_name)
        val_2 = getattr(entity_2, field_name)
        if isinstance(field_type, dict):
            recursive_compare(val_1, val_2, field_type)
        else:
            assert val_1 == val_2


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

    for baseline_paragraph, subject_paragraph in zip(
        baseline.paragraphs, subject.paragraphs
    ):
        recursive_compare(
            baseline_paragraph, subject_paragraph, paragraph_comparable_fields
        )
        for baseline_run, subject_run in zip(
            baseline_paragraph.runs, subject_paragraph.runs
        ):
            recursive_compare(baseline_run, subject_run, run_comparable_fields)
