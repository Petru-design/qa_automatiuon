import os
import shutil


def move_files(tests: list[str], source: str, target: str):
    for folder_name in tests:
        folder_path = os.path.join(source, folder_name)
        print(folder_name)
        for file_name in os.listdir(folder_path):
            if file_name == "images":
                continue
            file_ext = file_name.split(".")[-1]
            file_path = os.path.join(folder_path, file_name)

            baseline_target = os.path.join(target, file_ext, "baseline")
            if not os.path.exists(baseline_target):
                os.makedirs(baseline_target)
            shutil.copy(file_path, os.path.join(baseline_target, file_name))

            subject_target = os.path.join(target, file_ext, "subject")
            if not os.path.exists(subject_target):
                os.makedirs(subject_target)
            shutil.copy(file_path, os.path.join(subject_target, file_name))


def move_images(tests: list[str], source: str, target: str):
    for folder_name in tests:
        folder_path = os.path.join(source, folder_name, "images")
        if not os.path.exists(folder_path):
            continue
        print(folder_name)
        baseline_target = os.path.join(target, "jpg", "baseline", folder_name)
        subject_target = os.path.join(target, "jpg", "subject", folder_name)
        os.makedirs(baseline_target)
        os.makedirs(subject_target)
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            shutil.copy(file_path, os.path.join(baseline_target, file_name))
            shutil.copy(file_path, os.path.join(subject_target, file_name))


if __name__ == "__main__":
    source = "C:\\Users\\MKhimukhin\\export"
    target = "C:\\Space\\QAA\\data"
    tests = [
        name for name in os.listdir(source) if name not in ("templates", "Katalog5")
    ]
    move_files(tests, source, target)
    move_images(tests, source, target)
