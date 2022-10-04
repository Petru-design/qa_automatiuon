import os
from xmlrpc.client import FastMarshaller

from stiEF_tests.tests.pyfiles.text_similarity import TextSimilarly
from stiEF_tests.tests.pyfiles.image_similarity import StructuralSimilarity


def recursive_attribute_compare(
    entity_1,
    entity_2,
    template: dict[str, None | dict | type],
    current_path: list[str] | None = None,
):
    if current_path is None:
        current_path = []

    for field_name, field_type in template.items():
        val_1 = getattr(entity_1, field_name)
        val_2 = getattr(entity_2, field_name)
        if val_1 is None or val_2 is None:
            assert val_1 == val_2, (
                ".".join(current_path + [field_name]) + f" {val_1} != {val_2}"
            )
        elif isinstance(field_type, dict):
            current_path.append(field_name)
            recursive_attribute_compare(val_1, val_2, field_type, current_path)
            current_path.pop()
        else:
            assert val_1 == val_2, (
                ".".join(current_path + [field_name]) + f" {val_1} != {val_2}"
            )


def recursive_container_compare(val_1, val_2, current_path: list[str] | None = None):
    if current_path is None:
        current_path = []

    assert isinstance(val_1, type(val_2)), (
        ".".join(current_path) + f" type({val_1}) != type({val_2})"
    )
    if isinstance(val_1, (list, tuple)):
        assert len(val_1) == len(val_2), (
            ".".join(current_path) +
            f" different sizes: {len(val_1)} != {len(val_2)}"
        )
        for i, (elem_1, elem_2) in enumerate(zip(val_1, val_2)):
            current_path.append(f"[{i}]")
            recursive_container_compare(elem_1, elem_2, current_path)
            current_path.pop()
    elif isinstance(val_1, dict):
        assert set(val_1) == set(val_2), (
            ".".join(current_path) + " different keys in dicts"
        )
        for key in val_1:
            current_path.append(key)
            recursive_container_compare(val_1[key], val_2[key], current_path)
            current_path.pop()
    elif isinstance(val_1, str):
        assert val_1 == val_2, ".".join(current_path) + f" {val_1} != {val_2}"


def compare_texts(text_1, text_2, result_path):
    compare = TextSimilarly(text_1, text_2)
    _, score = compare.damerau_levenshtein()
    if score != 1:
        compare.write_comparation(result_path, sidebyside=False)
        assert (
            False
        ), f"Texts are not exactly the same, only for {score}. See output at {result_path}"


def compare_images(img_path_1, img_path_2, result_path, ext, naming_prefix) -> tuple[bool, str]:
    try:
        compare = StructuralSimilarity(img_path_1, img_path_2)
    except Exception as e:
        return (False, str(e))
    head, tail = os.path.split(result_path)
    result_path = os.path.join(head, naming_prefix + tail)
    if compare.score != 1:
        if not os.path.exists(result_path):
            os.makedirs(result_path)
        compare.save_images(result_path, ext,
                            True, True, True, True)
        return (False, f"Images are not exactly the same, only for {compare.score}. See output at {result_path}")

    return (True, "Images are exactly the same")
