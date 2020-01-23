import pytest

from client import put_data, post_data, get_data


def test_put_positive_message_and_queue():
    """Perform testing for PUT request. Make attempt to
    update message which was sent by POST request to specified queue

    ID: 60582c33-4b8e-4613-85b9-02ac691e412a

    Steps:
        1. Post message to a server
        2. Update this message using Put request
        3. Check that message was updated

    Expectedresults:
        1. Got updated message

    Importance: Critical
    """
    post_data(text_message='red', queue=55)
    put_data(text_message='blue', queue=55)
    assert get_data(queue=55) == 'blue'


def test_put_positive_message_without_queue():
    """Perform testing for PUT request. Make attempt to
    update message which was sent by POST request to default queue

    ID: 9ac7ff02-6d03-4f56-9854-df3f2b32ed3b

    Steps:
        1. Post message to a server
        2. Update this message using Put request
        3. Check that message was updated

    Expectedresults:
        1. Got updated message

    Importance: Critical
    """
    post_data(text_message='red', queue=0)
    put_data(text_message='blue')
    assert get_data(queue=0) == 'blue'


def test_put_negative_message_and_queue():
    """Perform testing for PUT request. Make attempt to
    update message when there is no message in the specified queue

    ID: 096b9f2d-0682-4e3f-a320-7f82c4f657e7

    Steps:
        1. Update message using Put request

    Expectedresults:
        1. Got 404 status code

    Importance: Critical
    """
    assert put_data(text_message='put', queue=0).status_code == 404


def test_put_negative_message_without_queue():
    """Perform testing for PUT request. Make attempt to
    update message when there is no message in the default queue

    ID: f1c72fe2-c3e1-4fde-b066-161540150aa5

    Steps:
        1. Update message using Put request

    Expectedresults:
        1. Got 404 status code

    Importance: Critical
    """
    assert put_data(text_message='put_without').status_code == 404


def test_put_negative_empty_message():
    """Perform testing for PUT request. Make attempt to
    update message which was sent by POST request to specified queue
    with empty message

    ID: 4aa727eb-1559-404a-b072-9d3f75092f7e

    Steps:
        1. Post message to a server
        2. Update this message using Put request with empty message

    Expectedresults:
        1. Got 'Message is empty' - message

    Importance: Critical
    """
    post_data(text_message='green')
    assert put_data(text_message='', queue=0) == 'Message is empty'


def test_put_positive_max_queues():
    """Perform testing for PUT request. Make attempt to
    update messages which was sent by POST request to specified queue,
    using 100 different queues

    ID: 930a2476-45af-46db-ae3d-3ea754b3a811

    Steps:
        1. 100 post messages to a server different queues
        2. Update this messages using Put request
        3. Check that messages was updated

    Expectedresults:
        1. Got updated messages

    Importance: Critical
    """
    for queue in range(100):
        post_data(text_message='cat', queue=queue)
        put_data(text_message='dog', queue=queue)
        assert get_data(queue=queue) == 'dog'


def test_put_positive_message_limit():
    """Perform testing for PUT request. Make attempt to
    update messages which was sent by POST request to specified queue,
    using default one queue and message max limit per server

    ID: baea5d72-4806-40b2-bebc-ee45b60e78ad

    Steps:
        1. 100 post messages to a server default one queue
        2. Update this messages using Put request
        3. Check that messages was updated

    Expectedresults:
        1. Got updated message

    Importance: Critical
    """
    for queue in range(100):
        post_data(text_message='cat', queue=0)
        put_data(text_message='dog', queue=0)
        assert get_data(queue=0) == 'dog'


@pytest.mark.parametrize('boundary', [-1, 10001, -10001])
def test_put_negative_unsupported_alias(boundary):
    """Perform testing for PUT request. Make attempt to
    update message which was sent by POST request to specified queue,
    using not allowed aliases value

    ID: f8188b5f-e122-4cf7-9339-a117399efdf3

    Steps:
        1. Update message using Put request on unsupported value

    Expectedresults:
        1. Got 'Unsupported alias' - message

    Importance: Critical
    """
    assert put_data(text_message='hi', queue=boundary) == 'Unsupported alias'


@pytest.mark.parametrize('over_100', [2222, 101, 9999])
def test_delete_positive_aliases_over_100(over_100):
    """Perform testing for PUT request. Make attempt to
    sent messages to the server using POST request to allowed
    aliases that bigger than 100, delete this messages and check
    that it was deleted

    ID: 5dc7641b-095c-4b74-92aa-612b94aadd7e

    Steps:
        1. POST request to allowed aliases that bigger than 100
        2. UPDATE this messages
        2. GET this messages

    Expectedresults:
        1. Got 'moon' messages

    Importance: Critical
    """
    post_data(text_message='sun', queue=over_100)
    put_data(text_message='moon', queue=over_100)
    assert get_data(queue=over_100) == 'moon'
