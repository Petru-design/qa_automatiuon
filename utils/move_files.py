import argparse
import os
import shutil


def safe_copy(src_path: str, dst_folder_path: str, file_name: str):
    if not os.path.exists(dst_folder_path):
        os.makedirs(dst_folder_path)
    shutil.copy(src_path, os.path.join(dst_folder_path, file_name))


def copy_file(
    file_name: str,
    folder_path: str,
    target: str,
    as_base: bool,
    as_subject: bool,
):
    file_name_raw, file_ext = file_name.split(".")
    src_path = os.path.join(folder_path, file_name)
    dst_path = os.path.join(target, file_ext, file_name_raw)
    if as_base:
        safe_copy(src_path, dst_path, f"baseline.{file_ext}")
    if as_subject:
        safe_copy(src_path, dst_path, f"subject.{file_ext}")


def copy_image(
    test_name: str,
    file_name: str,
    folder_path: str,
    target: str,
    as_base: bool,
    as_subject: bool,
):
    file_ext = file_name.split(".")[-1]
    src_path = os.path.join(folder_path, file_name)
    if as_base:
        basline_dst_path = os.path.join(target, file_ext, test_name, "baseline")
        safe_copy(src_path, basline_dst_path, file_name)
    if as_subject:
        subject_dst_path = os.path.join(target, file_ext, test_name, "subject")
        safe_copy(src_path, subject_dst_path, file_name)


def move_files(
    tests: list[str],
    source: str,
    target: str,
    as_base: bool = False,
    as_subject: bool = False,
):
    for folder_name in tests:
        folder_path = os.path.join(source, folder_name)
        for file_name in os.listdir(folder_path):
            if file_name == "images":
                continue
            copy_file(file_name, folder_path, target, as_base, as_subject)
        images_path = os.path.join(folder_path, "images")
        if not os.path.exists(images_path):
            continue
        for file_name in os.listdir(images_path):
            copy_image(folder_name, file_name, images_path, target, as_base, as_subject)


def read_tests(source_path: str, test_names: list[str] | None) -> list[str]:
    if test_names:
        return [name for name in os.listdir(source_path) if name in test_names]
    return [
        name
        for name in os.listdir(source_path)
        if name not in ("templates", "Katalog5", "generic_json")
    ]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "source_path",
        nargs="?",
        help="Path to copy files from.",
    )
    parser.add_argument(
        "target_path",
        nargs="?",
        help="Path to copy file to.",
    )
    parser.add_argument(
        "tests",
        nargs="*",
        help="List of tests names to copy. If empty, copy all the data in source.",
    )
    parser.add_argument(
        "--as_base",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Copy files as baseline test data. Default is False.",
    )
    parser.add_argument(
        "--as_subject",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Copy files as test subjects. Default is False.",
    )

    args = parser.parse_args()
    tests = read_tests(args.source_path, args.tests)
    move_files(tests, args.source_path, args.target_path, args.as_base, args.as_subject)
