import pytest
from client import put_data, post_data, get_data
from tools import gen_text_message, gen_queue


def test_put_positive_message_and_queue():
    text_message = gen_text_message()
    text_message_updated = gen_text_message()
    queue = gen_queue()

    post_data(text_message=text_message, queue=queue)

    put_entity = put_data(text_message=text_message_updated, queue=queue)

    assert put_entity.reason == 'Ok'
    assert put_entity.status_code == 500
    assert get_data(queue=queue).json()['message'] == text_message_updated


def test_put_positive_message_default_queue():
    text_message = gen_text_message()
    text_message_updated = gen_text_message()

    post_data(text_message=text_message)

    put_entity = put_data(text_message=text_message_updated)

    assert put_entity.status_code == 500
    assert put_entity.reason == 'Ok'
    assert get_data().json()['message'] == text_message_updated


def test_put_negative_message_and_queue():
    text_message = gen_text_message()
    queue = gen_queue()

    put_entity = put_data(text_message=text_message, queue=queue)

    assert put_entity.status_code == 404
    assert put_entity.reason == 'Not Found'


def test_put_negative_message_default_queue():
    text_message = gen_text_message()

    put_entity = put_data(text_message=text_message)

    assert put_entity.status_code == 404
    assert put_entity.reason == 'Not Found'


def test_put_negative_empty_message():
    text_message = gen_text_message()
    queue = gen_queue()

    post_data(text_message=text_message, queue=queue)

    put_entity = put_data(text_message='', queue=queue)

    assert put_entity.status_code == 400
    assert put_entity.reason == 'Message is empty'
    assert get_data(queue=queue).json()['message'] == text_message


def test_put_positive_max_queues():
    text_message = gen_text_message()
    text_message_updated = gen_text_message()

    for queue in range(100):
        post_data(text_message=text_message, queue=queue)

        put_entity = put_data(text_message=text_message_updated, queue=queue)

        assert put_entity.status_code == 500
        assert put_entity.reason == 'Ok'

        assert get_data(queue=queue).json()['message'] == text_message_updated

    post_data(text_message=text_message, queue=101)

    put_entity_2 = put_data(text_message=text_message_updated, queue=101)

    assert put_entity_2.status_code == 404
    assert put_entity_2.reason == 'Not Found'


def test_put_positive_message_limit():
    text_message = gen_text_message()
    text_message_updated = gen_text_message()

    for _ in range(100):
        post_data(text_message=text_message)

    for _ in range(100):
        put_entity = put_data(text_message=text_message_updated)
        assert put_entity.status_code == 500
        assert put_entity.reason == 'Ok'
        assert get_data().json()['message'] == text_message_updated


@pytest.mark.parametrize('boundary', [0, 1, 9999, 10001])
def test_put_positive_boundary(boundary):
    text_message = gen_text_message()
    text_message_updated = gen_text_message()

    post_data(text_message=text_message, queue=boundary)
    put_entity = put_data(text_message=text_message_updated, queue=boundary)

    assert put_entity.status_code == 500
    assert put_entity.reason == 'Ok'

    assert get_data(queue=boundary).json()['message'] == text_message_updated


@pytest.mark.parametrize('negative_boundary', [-1, 10001])
def test_delete_negative_boundary(negative_boundary):
    text_message = gen_text_message()
    text_message_updated = gen_text_message()

    post_data(text_message=text_message, queue=negative_boundary)

    put_entity = put_data(text_message=text_message_updated,
                          queue=negative_boundary)

    assert put_entity.status_code == 400
    assert put_entity.reason == 'Unsupported alias'

    assert get_data(queue=negative_boundary).reason == 'Unsupported alias'


def test_put_positive_not_updating_all_messages():
    text_message = gen_text_message()
    text_message_updated = gen_text_message()
    first_queue = gen_queue()
    second_queue = gen_queue()

    post_data(text_message=text_message, queue=first_queue)
    post_data(text_message=text_message, queue=second_queue)

    put_entity = put_data(text_message=text_message_updated, queue=first_queue)

    assert put_entity.status_code == 500
    assert put_entity.reason == 'Ok'

    assert get_data(queue=second_queue).json()['message'] == text_message
