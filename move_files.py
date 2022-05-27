import os
import shutil


def safe_copy(file_path: str, full_target_path: str, file_name: str):
    if not os.path.exists(full_target_path):
        os.makedirs(full_target_path)
    shutil.copy(file_path, os.path.join(full_target_path, file_name))


def copy_file(file_name: str, folder_path: str, target: str):
    file_ext = file_name.split(".")[-1]
    file_path = os.path.join(folder_path, file_name)

    safe_copy(file_path, os.path.join(target, file_ext, "baseline"), file_name)
    safe_copy(file_path, os.path.join(target, file_ext, "subject"), file_name)


def copy_image(test_name: str, file_name: str, folder_path: str, target: str):
    file_ext = file_name.split(".")[-1]
    file_path = os.path.join(folder_path, file_name)

    safe_copy(
        file_path, os.path.join(target, file_ext, "baseline", test_name), file_name
    )
    safe_copy(
        file_path, os.path.join(target, file_ext, "subject", test_name), file_name
    )


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
