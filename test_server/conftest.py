from time import sleep
import subprocess
import pytest


@pytest.fixture(scope='session', autouse=True)
def run_stop_server():
    """Fixture for starting server before test_server and stop it after test is done

    :return: None
    """
    process = subprocess.Popen('python3 /Users/phavry/Desktop/rest_client/server.py',
                               shell=True)
    sleep(2)

    yield
    process.kill()

