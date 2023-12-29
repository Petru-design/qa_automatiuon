import os
import signal
import psutil
import json
import subprocess
import threading
import logging


def kill_all_pythons():
    # kill all python processes except current process
    current_process_id = os.getpid()
    all_ids = [p.pid for p in psutil.process_iter() if p.name()
               == 'python.exe']
    for id in all_ids:
        if id != current_process_id:
            os.kill(id, signal.SIGTERM)


def start_serving_frontend():

    # python -m http.server --directory C:\Costum\Work\qa_automation\dist 8100
    command = ['python', '-m', 'http.server', '--directory',
               os.path.join(os.path.dirname(__file__), r'dist'), '8100']
    threading.Thread(target=subprocess.run, args=(command,)).start()


def get_home_dir():
    user_home_dir = os.environ.get('USER_HOME')
    if user_home_dir is None:
        user_home_dir = os.environ.get('HOME')
    if user_home_dir is None:
        user_home_dir = os.environ.get('HOMEPATH')
    if user_home_dir is None:
        user_home_dir = os.environ.get('HOMEDRIVE')
    if user_home_dir is None:
        user_home_dir = os.environ.get('USERPROFILE')
    if user_home_dir is None:
        user_home_dir = os.path.expanduser('~')
    return user_home_dir


def read_config_file(config_file_path):
    with open(config_file_path, 'r') as f:
        config = json.load(f)
    return config


def create_config_file():
    user_home_dir = get_home_dir()

    stief_dir = os.path.join(user_home_dir, "stief")
    if not os.path.exists(stief_dir):
        os.makedirs(stief_dir)

    config_file_path = os.path.join(os.path.dirname(__file__), "config.json")

    config = {
        "defaultCatalogsCsvFile": os.path.join(stief_dir, "defaultCatalogs.csv"),
        "exportDirectory": os.path.join(stief_dir, "testoutput"),
        "baselineDirectory": os.path.join(stief_dir, "baselines"),
        "outputDirectory":  os.path.join(stief_dir, "results")
    }

    with open(config_file_path, 'w') as f:
        json.dump(config, f, indent=4)


async def update_config_file(config_file_path: str,  paths: dict) -> None:
    print("Updating config file")
    with open(config_file_path, 'w') as f:
        json.dump(paths, f, indent=4)


def check_baselines(baseline_directory: str,
                    catalog_name: str,
                    extension: str) -> bool:
    if extension in ["jpg", "png"]:
        baseline_path = os.path.join(baseline_directory,
                                     catalog_name, "images")
    else:
        baseline_path = os.path.join(baseline_directory, catalog_name, f"{
                                     catalog_name}.{extension}")
    return os.path.exists(baseline_path)
