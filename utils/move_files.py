import os
import shutil


def safe_copy(src_path: str, dst_folder_path: str, file_name: str):
    if not os.path.exists(dst_folder_path):
        os.makedirs(dst_folder_path)
    shutil.copy(src_path, os.path.join(dst_folder_path, file_name))


def copy_file(file_name: str, folder_path: str, target: str):
    file_name_raw, file_ext = file_name.split(".")
    src_path = os.path.join(folder_path, file_name)
    dst_path = os.path.join(target, file_ext, file_name_raw)

    safe_copy(src_path, dst_path, f"baseline.{file_ext}")
    safe_copy(src_path, dst_path, f"subject.{file_ext}")


def copy_image(test_name: str, file_name: str, folder_path: str, target: str):
    file_ext = file_name.split(".")[-1]
    src_path = os.path.join(folder_path, file_name)
    basline_dst_path = os.path.join(target, file_ext, test_name, "baseline")
    subject_dst_path = os.path.join(target, file_ext, test_name, "subject")

    safe_copy(src_path, basline_dst_path, file_name)
    safe_copy(src_path, subject_dst_path, file_name)


def move_files(tests: list[str], source: str, target: str):
    for folder_name in tests:
        folder_path = os.path.join(source, folder_name)
        for file_name in os.listdir(folder_path):
            if file_name == "images":
                continue
            copy_file(file_name, folder_path, target)
        images_path = os.path.join(folder_path, "images")
        if not os.path.exists(images_path):
            continue
        for file_name in os.listdir(images_path):
            copy_image(folder_name, file_name, images_path, target)


if __name__ == "__main__":
    source = "C:\\Users\\MKhimukhin\\export"
    target = "C:\\Space\\QAA\\data"
    tests = [
        name
        for name in os.listdir(source)
        if name not in ("templates", "Katalog5", "generic_json")
    ]
    move_files(tests, source, target)
