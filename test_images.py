import os

import pytest

from utils.navigation import paths_keeper
from pyfiles.image_similarity import StructuralSimilarity


@pytest.mark.parametrize(
    "test_path",
    paths_keeper.get_paths("jpg"),
    ids=paths_keeper.get_ids("jpg"),
)
def test_jpg(test_path):
    baseline_path = os.path.join(test_path, "baseline")
    subject_path = os.path.join(test_path, "subject")

    for baseline_image_path, subject_image_path in zip(
        os.listdir(baseline_path), os.listdir(subject_path)
    ):
        compare = StructuralSimilarity(
            os.path.join(baseline_path, baseline_image_path),
            os.path.join(subject_path, subject_image_path),
        )
        assert compare.score == 1


@pytest.mark.parametrize(
    "test_path",
    paths_keeper.get_paths("png"),
    ids=paths_keeper.get_ids("png"),
)
def test_png(test_path):
    baseline_path = os.path.join(test_path, "baseline")
    subject_path = os.path.join(test_path, "subject")

    for baseline_image_path, subject_image_path in zip(
        os.listdir(baseline_path), os.listdir(subject_path)
    ):
        compare = StructuralSimilarity(
            os.path.join(baseline_path, baseline_image_path),
            os.path.join(subject_path, subject_image_path),
        )
        assert compare.score == 1
