
def pytest_addoption(parser):
    parser.addoption("--name", action="store")
    parser.addoption("--subject", action="store")
    parser.addoption("--reference", action="store")
    parser.addoption("--results", action="store")
    parser.addoption("--config_path", action="store", default="config.json")
