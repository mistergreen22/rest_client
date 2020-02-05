import os
from time import sleep
import subprocess
import pytest
server_path = os.path.abspath("../server.py")


@pytest.fixture(scope='function', autouse=True)
def run_stop_server():
    """Fixture for starting server before test_server and stop it after
    test is done

    :return: None
    """
    process = subprocess.Popen(f'python3 {server_path}',
                               shell=True)
    sleep(2)

    yield
    process.kill()
