from time import sleep
import subprocess
import pytest
from client import delete_data


@pytest.fixture(scope='session', autouse=True)
def run_stop_server():
    """Fixture for starting server before tests and stop it after test is done

    :return: None
    """
    process = subprocess.Popen('python3 /Users/phavry/Desktop/rest_client/server.py',
                               shell=True)
    sleep(2)

    yield
    process.kill()


@pytest.fixture(scope='function', autouse=True)
def clear_data_on_server():
    """Fixture for cleaning data before every function

    :return: None
    """
    for i in range(100):
        for y in range(100):
            delete_data(queue=y)
