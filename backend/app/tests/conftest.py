def pytest_configure(config):
    # register an additional marker
    config.addinivalue_line("markers", "currently_playing")
    config.addinivalue_line("markers", "client")
