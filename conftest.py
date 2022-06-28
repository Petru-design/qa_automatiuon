
def pytest_addoption(parser):
    parser.addoption("--scenario_name", action="store")
    parser.addoption("--scenario_path", action="store")
    parser.addoption("--baseline_path", action="store")
    parser.addoption("--result_path", action="store")
    parser.addoption("--config_path", action="store", default="./config.json")
