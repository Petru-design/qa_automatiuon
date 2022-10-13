import os

from stiEF_tests.tests.utils.comparators import compare_images


def test_jpg(reference_path, subject_path, result_path, naming_prefix):
    baseline_images = sorted(
        path for path in os.listdir(reference_path) if path.endswith(".jpg")
    )
    subject_images = sorted(
        path for path in os.listdir(subject_path) if path.endswith(".jpg")
    )

    error_list = []
    for subject_image_path in subject_images:
        if subject_image_path not in baseline_images:
            print("skipping ", subject_image_path)
            error_list.append(
                f"Image {subject_image_path} not found in baseline")
            continue
        result = compare_images(
            os.path.join(reference_path, subject_image_path),
            os.path.join(subject_path, subject_image_path),
            os.path.join(result_path, "result",
                         subject_image_path.split(".")[0]),
            "JPG",
            naming_prefix,
        )

        if not result[0]:
            error_list.append(result[1])

    assert not error_list, "Issues detected:\n" + "\n".join(error_list)


def test_png(reference_path, subject_path, result_path, naming_prefix):
    baseline_images = sorted(
        path for path in os.listdir(reference_path) if path.endswith(".png")
    )
    subject_images = sorted(
        path for path in os.listdir(subject_path) if path.endswith(".png")
    )

    error_list = []
    for subject_image_path in subject_images:
        if subject_image_path not in baseline_images:
            print("skipping ", subject_image_path)
            error_list.append(
                f"Image {subject_image_path} not found in baseline")
            continue
        result = compare_images(
            os.path.join(reference_path, subject_image_path),
            os.path.join(subject_path, subject_image_path),
            os.path.join(result_path, "result",
                         subject_image_path.split(".")[0]),
            "PNG",
            naming_prefix,
        )

        if not result[0]:
            error_list.append(result[1])

    assert not error_list, "Issues detected:\n" + "\n\n".join(error_list)
