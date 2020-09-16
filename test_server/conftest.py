import os
from time import sleep
import subprocess
import pytest
server_path = os.path.abspath("../server.py")


@pytest.fixture(scope='function')
def run_stop_server_function():
    process = None

    def _fixtures_arguments(port=None):
        command = f'python3 {server_path}'
        if port is not None:
            command = ''.join((
                command,
                f' -p {port}'
            ))
        nonlocal process
        process = subprocess.Popen(command, shell=True)
        sleep(2)

    yield _fixtures_arguments

    if process is not None:
        process.kill()


@pytest.fixture(scope='module')
def run_stop_server_module():
    processes = []

    def _fixtures_arguments(port=None):
        command = f'python3 {server_path}'
        if port is not None:
            command = ''.join((
                command,
                f' -p {port}'
            ))
        processes.append(subprocess.Popen(command, shell=True))
        sleep(2)

    yield _fixtures_arguments

    processes[0].kill()
