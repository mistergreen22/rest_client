import pytest
import requests
from client import post_data, delete_data
from tools import gen_text_message, gen_queue


@pytest.mark.parametrize('forbidden_port', [1023, 49152, 0, -1024])
def test_negative_boundary(run_stop_server_function, forbidden_port):
    run_stop_server_function(port=forbidden_port)
    with pytest.raises(requests.exceptions.ConnectionError):
        delete_data(forbidden_port)


@pytest.mark.parametrize('allowed_port', [1024, 1025, 49150, 49151])
def test_positive_boundary(run_stop_server_function, allowed_port):
    run_stop_server_function(port=allowed_port)
    message = gen_text_message()
    queue = gen_queue()
    assert post_data(text_message=message, queue=queue, port=allowed_port
                     ).raw._pool.port == allowed_port


def test_default_port(run_stop_server_module):
    run_stop_server_module()
    message = gen_text_message()
    queue = gen_queue()
    assert post_data(text_message=message, queue=queue).raw._pool.port == 8888
