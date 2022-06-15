import os

import pytest

from utils.navigation import paths_keeper
from utils.comparators import compare_images


@pytest.mark.parametrize(
    "baseline_path,subject_path,result_path",
    paths_keeper.get_paths("jpg"),
    ids=paths_keeper.get_ids("jpg"),
)
def test_jpg(baseline_path, subject_path, result_path):

    baseline_images = sorted(
        path for path in os.listdir(baseline_path) if path.endswith(".jpg")
    )
    subject_images = sorted(
        path for path in os.listdir(subject_path) if path.endswith(".jpg")
    )
    for baseline_image_path, subject_image_path in zip(baseline_images, subject_images):
        compare_images(
            os.path.join(baseline_path, baseline_image_path),
            os.path.join(subject_path, subject_image_path),
            os.path.join(result_path, "result", subject_image_path.split(".")[0]),
            "JPG",
        )


@pytest.mark.parametrize(
    "baseline_path,subject_path,result_path",
    paths_keeper.get_paths("png"),
    ids=paths_keeper.get_ids("png"),
)
def test_png(baseline_path, subject_path, result_path):

    baseline_images = sorted(
        path for path in os.listdir(baseline_path) if path.endswith(".png")
    )
    subject_images = sorted(
        path for path in os.listdir(subject_path) if path.endswith(".png")
    )
    for baseline_image_path, subject_image_path in zip(baseline_images, subject_images):
        compare_images(
            os.path.join(baseline_path, baseline_image_path),
            os.path.join(subject_path, subject_image_path),
            os.path.join(result_path, "result", subject_image_path.split(".")[0]),
            "PNG",
        )
