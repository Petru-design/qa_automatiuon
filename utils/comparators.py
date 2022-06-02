import os

from pyfiles.text_similarity import TextSimilarly
from pyfiles.image_similarity import StructuralSimilarity


def recursive_attribute_compare(
    entity_1, entity_2, template: dict[str, None | dict | type]
):
    for field_name, field_type in template.items():
        val_1 = getattr(entity_1, field_name)
        val_2 = getattr(entity_2, field_name)
        if val_1 is None or val_2 is None:
            assert val_1 == val_2
        elif isinstance(field_type, dict):
            recursive_attribute_compare(val_1, val_2, field_type)
        else:
            assert val_1 == val_2


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


def compare_texts(text_1, text_2, result_path):
    compare = TextSimilarly(text_1, text_2)
    _, score = compare.damerau_levenshtein()
    if score != 1:
        compare.write_comparation(result_path, sidebyside=False)
        assert (
            False
        ), f"Texts are not exactly the same, only for {score}. See output at {result_path}"


def compare_images(img_path_1, img_path_2, result_path, ext):
    compare = StructuralSimilarity(img_path_1, img_path_2)
    if compare.score != 1:
        if not os.path.exists(result_path):
            os.makedirs(result_path)
        compare.save_images(result_path, ext, True, True, True, True)
        assert (
            False
        ), f"Images are not exactly the same, only for {compare.score}. See output at {result_path}"
