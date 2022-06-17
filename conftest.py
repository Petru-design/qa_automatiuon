def pytest_addoption(parser):
    parser.addoption("--scenario_path", action="store")
    parser.addoption("--baseline_path", action="store")
    parser.addoption("--result_path", action="store")