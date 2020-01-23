import pytest
from client import post_data, get_data, delete_data


def test_post_positive_message_and_queue():
    """Perform testing for POST request. Make attempt to
    sent message to the server using POST request to specified queue

    ID: 2ccf45e2-f4a4-4b35-98be-459ee3279d8d

    Steps:
        1. Post message to a server

    Expectedresults:
        1. Got status code 201

    Importance: Critical
    """
    assert post_data(text_message='post_with', queue=33).status_code == 201


def test_post_positive_message_without_queue():
    """Perform testing for POST request. Make attempt to
    sent message to the server using POST request to default queue

    ID: 3866b26c-516d-4cf5-b33f-dd1da8894c87

    Steps:
        1. Post message to a server

    Expectedresults:
        1. Got status code 201

    Importance: Critical
    """
    assert post_data(text_message='post_without').status_code == 201
    delete_data()


def test_post_negative_empty_message_without_queue():
    """Perform testing for POST request. Make attempt to
    sent empty message to the server using POST request to default queue

    ID: 3673bd1f-1844-4d22-bb15-3bfa53deb186

    Steps:
        1. Post empty message to a server

    Expectedresults:
        1. Got status code 400

    Importance: Critical
    """
    assert post_data(text_message='').status_code == 400


def test_post_negative_empty_message_with_queue():
    """Perform testing for POST request. Make attempt to
    sent empty message to the server using POST request to specified queue

    ID: a4e12dec-83c6-49c2-8f80-e2d269f85d7f

    Steps:
        1. Post empty message to a server

    Expectedresults:
        1. Got status code 400

    Importance: Critical
    """
    assert post_data(text_message='', queue=0).status_code == 400


@pytest.mark.parametrize('boundary', [-1, 10001, -10001])
def test_post_negative_unsupported_alias(boundary):
    """Perform testing for POST request. Make attempt to
    sent message to the server using POST request to unsupported aliases value

    ID: de277ca7-2c37-4f43-bcdd-3f6727318843

    Steps:
        1. Post messages to a server with unsupported queue value

    Expectedresults:
        1. Got status code 400

    Importance: Critical
    """
    assert post_data(text_message='post_unsupported_alias', queue=boundary).status_code == 400


def test_post_positive_max_queues():
    """Perform testing for POST request. Make attempt to
    sent messages to the server using POST request to 100 different queues

    ID: 47394a45-52ba-4d75-9899-a618ebc59369

    Steps:
        1. Post messages to 100 different queues

    Expectedresults:
        1. Got status code 201

    Importance: Critical
    """
    for queue in range(100):
        assert post_data(text_message='post_max', queue=queue).status_code == 201
        delete_data(queue=queue)


def test_post_positive_message_limit():
    """Perform testing for POST request. Make attempt to
    sent 100 messages to the server using POST request to default one queue

    ID: 2c2c793f-aa49-4a60-864f-f52cc568a9e4

    Steps:
        1. Post messages to 100 messages to default queues

    Expectedresults:
        1. Got status code 201

    Importance: Critical
    """
    for queue in range(100):
        assert post_data(text_message='post_limit', queue=0).status_code == 201
        delete_data()


def test_post_positive_ignore_message():
    """Perform testing for POST request. Make attempt to
    sent 100 messages to the server using POST request to default one queue,
    then send one more and check that 101 message will be ignored

    ID: 3df80728-4a10-43b2-98f1-82e82e1bef0f

    Steps:
        1. Post messages to 100 messages to one queues
        2. Post one more messages
        3. Get last message from the queue

    Expectedresults:
        1. Got first type message because last one must be ignored

    Importance: Critical
    """
    for queue in range(100):
        post_data(text_message='post_permissible', queue=7)

    post_data(text_message='post_out_of_range', queue=7)

    assert get_data(queue=7) == 'post_permissible'
