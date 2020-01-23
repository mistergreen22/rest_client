import pytest

from client import post_data, delete_data, get_data
from tools import volume


def test_delete_positive_with_queue():
    """Perform testing for DELETE request. Make attempt to
    sent message to the server using POST request to specified queue,
    delete this message and check that it was deleted

    ID: 7221dbb9-2bcb-4cb3-b1ab-422fe6b599c6

    Steps:
        1. Post request with this message to a server
        2. Delete request to specified queue
        2. Try to Get deleted message from specified queue

    Expectedresults:
        1. Got 'no messages' because the message was deleted

    Importance: Critical
    """
    post_data('delete', 22)
    assert delete_data(queue=22).status_code == 204
    assert get_data(queue=22) == 'no messages'


def test_delete_positive_without_queue():
    """Perform testing for DELETE request. Make attempt to
    sent message to the server using POST request to default queue,
    delete this message(not specifying the queue) and check that it was deleted

    ID: 16b1abf8-6e80-4eff-a9b9-27981a79afb6

    Steps:
        1. Post request with this message to a server
        2. Delete request to specified queue
        2. Try to Get deleted message from specified queue

    Expectedresults:
        1. Got 'no messages' because the message was deleted

    Importance: Critical
    """
    post_data('delete', 0)
    assert delete_data().status_code == 204
    assert get_data(queue=0) == 'no messages'


def test_delete_negative_with_queue():
    """Perform testing for DELETE request. Make attempt to
    delete message from empty specified queue

    ID: 4cd161d6-14d5-4fd8-bdaa-e7fa27232465

    Steps:
        1. Delete request to specified queue

    Expectedresults:
        1. Got 404 status code because the queue is empty

    Importance: Critical
    """
    assert delete_data(queue=66).status_code == 404


def test_delete_negative_without_queue():
    """Perform testing for DELETE request. Make attempt to
    delete message from empty default queue(not specifying the queue)

    ID: 5dcda8fc-fae4-46c8-a51e-7593fd8ac95d

    Steps:
        1. Delete request to default queue

    Expectedresults:
        1. Got 404 status code because the queue is empty

    Importance: Critical
    """
    assert delete_data().status_code == 404


@pytest.mark.parametrize("aliases", volume())
def test_delete_negative_aliases(aliases):
    """Perform testing for DELETE request. Make attempt to
    delete messages from empty queue with all supported aliases

    ID: 74c2b1c1-ec95-4edc-a2d1-01694992122b

    Steps:
        1. Delete request with all supported aliases

    Expectedresults:
        1. Got 404 status code because the queue is empty

    Importance: Critical
    """
    assert delete_data(queue=aliases).status_code == 404


def test_delete_positive_max_queue():
    """Perform testing for DELETE request. Make attempt to
    delete messages which was sent by POST request to specified queue,
    using 100 different queues

    ID: 57a0114d-9a21-4bc6-8b84-2332d4992eb3

    Steps:
        1. 100 post messages to a server different queues
        2. Delete this messages using DELETE request
        3. Check that messages was deleted

    Expectedresults:
        1. Got 'no messages'

    Importance: Critical
    """
    for queue in range(100):
        post_data(text_message='hundred_get', queue=queue)
        delete_data(queue=queue)
        assert get_data(queue=queue) == 'no messages'


def test_delete_positive_message_limit():
    """Perform testing for DELETE request. Make attempt to
    delete messages which was sent by POST request to specified queue,
    using default one queue and message max limit per server

    ID: be1c78ad-66e0-4ae7-9dd3-517f7f8267b1

    Steps:
        1. 100 post messages to a server default one queue
        2. DELETE this messages using Delete request
        3. Check that messages was deleted

    Expectedresults:
        1. Got 'no messages'

    Importance: Critical
    """
    for queue in range(100):
        post_data(text_message='hundred_get', queue=0)
        delete_data(queue=0)
        assert get_data(queue=0) == 'no messages'


@pytest.mark.parametrize('boundary', [-1, 10001, -10001])
def test_delete_negative_unsupported_aliases(boundary):
    """Perform testing for DELETE request. Make attempt to
    delete messages which was sent by POST request to specified queue,
    using not allowed aliases value

    ID: 9654d566-ea19-4897-9461-74c660a28936

    Steps:
        1. Delete message using Put request on unsupported value

    Expectedresults:
        1. Got 400 status code

    Importance: Critical
    """
    assert delete_data(queue=boundary).status_code == 400


@pytest.mark.parametrize('over_100', [2222, 101, 9999])
def test_delete_positive_aliases_over_100(over_100):
    """Perform testing for DELETE request. Make attempt to
    sent messages to the server using POST request to allowed
    aliases that bigger than 100, delete this messages and check
    that it was deleted

    ID: 7cebace6-6da9-48cc-85f0-b669fa1e0267

    Steps:
        1. POST request to allowed aliases that bigger than 100
        2. DELETE this messages
        2. Get this messages

    Expectedresults:
        1. Got 'no messages'

    Importance: Critical
    """
    post_data(text_message='brown_code', queue=over_100)
    delete_data(queue=over_100)
    assert get_data(queue=over_100) == 'no messages'
