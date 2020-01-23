import pytest

from client import post_data, get_data


def test_get_positive_message_and_queue():
    """Perform testing for GET request. Make attempt to
    sent message to the server using POST request to specified queue
    and get this message after

    ID: 11ce3afa-76ee-497d-bdd7-b2085047ae37

    Steps:
        1. Post request with this message to a server
        2. Get request to a server with specified queue

    Expectedresults:
        1. Got this message

    Importance: Critical
    """
    post_data(text_message='get', queue=0)
    assert get_data(queue=0) == 'get'


def test_get_positive_message_without_queue():
    """Perform testing for GET request. Make attempt to
    sent message to the server using POST request to default queue
    and get this message after(not specify queue, leave empty)

    ID: 90f89828-0ee9-4f70-ad48-614f494fd198

    Steps:
        1. Post request with this message to a server
        2. Get request to a server with not specified queue

    Expectedresults:
        1. Got this message

    Importance: Critical
    """
    post_data(text_message='get_without', queue=0)
    assert get_data() == 'get_without'


def test_get_positive_delete_message():
    """Perform testing for GET request. Make attempt to
    sent message to the server using POST request, get this message after
    and try to get this message again

    ID: 61de72cd-cc70-4bd2-a34f-746f8fbebb8f

    Steps:
        1. Post request with this message to a server
        2. Get request to a server
        3. Get request to a server again

    Expectedresults:
        1. Got 'no messages' because it was deleted

    Importance: Critical
    """
    post_data(text_message='get_delete', queue=55)
    assert get_data(queue=55) == 'get_delete'
    assert get_data(queue=55) == 'no messages'


def test_get_positive_empty_queue():
    """Perform testing for GET request. Make attempt to
    get message from empty queue

    ID: 6a6d7b60-d65f-4f6e-8536-db0861f9066f

    Steps:
        1. Get request to a server

    Expectedresults:
        1. Got 'no messages' because queue is empty

    Importance: Critical
    """
    assert get_data(queue=0) == 'no messages'


@pytest.mark.parametrize('boundary', [-1, -10001, 10001])
def test_get_negative_unsupported_aliases(boundary):
    """Perform testing for GET request. Make attempt to
    get messages from the server using GET request from empty queue
    to unsupported aliases value

    ID: 92b5c3b3-b747-4521-a306-b08c34f334eb

    Steps:
        1. GET request to a server with unsupported queue value

    Expectedresults:
        1. Got 'Queue must be <= 10000' - message

    Importance: Critical
    """
    assert get_data(queue=boundary) == 'Queue must be <= 10000'


def test_get_positive_max_queues():
    """Perform testing for GET request. Make attempt to
    sent messages to the server using POST request to 100 different queues
    and get this messages after

    ID: 62de409f-52f5-4059-bc3b-e473a26d63f1

    Steps:
        1. Post messages to 100 different queues
        2. Get this messages from 100 different queues

    Expectedresults:
        1. Got status code 201

    Importance: Critical
    """
    for queue in range(100):
        post_data(text_message='get_queues', queue=queue)
        assert get_data(queue=queue) == 'get_queues'


def test_get_positive_message_limit():
    """Perform testing for GET request. Make attempt to
    sent 100 messages to the server using POST request to default one queue
    and get this messages after

    ID: 45851574-e5c6-4947-9baa-739022fc7802

    Steps:
        1. Post 100 messages default queues
        2. Get this messages from default queues

    Expectedresults:
        1. Got 100 messages that was sent

    Importance: Critical
    """
    for queue in range(100):
        post_data(text_message='get_limit', queue=0)
        assert get_data(queue=0) == 'get_limit'


@pytest.mark.parametrize('over_100', [2222, 101, 9999])
def test_get_positive_aliases_over_100(over_100):
    """Perform testing for GET request. Make attempt to
    sent messages to the server using POST request to allowed
    aliases that bigger than 100 and get this messages after

    ID: e8908ef6-5920-4f10-8b5c-05aee60efdc0

    Steps:
        1. POST request to allowed aliases that bigger than 100
        2. Get this messages

    Expectedresults:
        1. Got messages that was sent

    Importance: Critical
    """
    post_data(text_message='brown_code', queue=over_100)
    assert get_data(queue=over_100) == 'brown_code'
