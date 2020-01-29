import pytest
from client import put_data, post_data, get_data
from tools import gen_text_message, gen_queue


def test_put_positive_message_and_queue():
    text_message = gen_text_message()
    text_message_updated = gen_text_message()
    queue = gen_queue()

    post_data(text_message=text_message, queue=queue)
    assert put_data(text_message=text_message_updated, queue=queue).status_code == 500
    assert get_data(queue=queue).json()['message'] == text_message_updated


def test_put_positive_message_without_queue():
    text_message = gen_text_message()
    text_message_updated = gen_text_message()

    post_data(text_message=text_message)
    assert put_data(text_message=text_message_updated).status_code == 500
    assert get_data().json()['message'] == text_message_updated


def test_put_negative_message_and_queue():
    text_message = gen_text_message()
    queue = gen_queue()

    assert put_data(text_message=text_message, queue=queue).status_code == 404


def test_put_negative_message_without_queue():
    text_message = gen_text_message()

    assert put_data(text_message=text_message).status_code == 404


def test_put_negative_empty_message():
    text_message = gen_text_message()
    queue = gen_queue()

    post_data(text_message=text_message, queue=queue)
    assert put_data(text_message='', queue=queue).status_code == 500
    assert get_data(queue=queue).json()['message'] == ''


def test_put_positive_max_queues():
    text_message = gen_text_message()
    text_message_updated = gen_text_message()

    for queue in range(100):
        post_data(text_message=text_message, queue=queue)

    for queue in range(100):
        assert put_data(text_message=text_message_updated, queue=queue).status_code == 500

    for queue in range(100):
        assert get_data(queue=queue).json()['message'] == text_message_updated


def test_put_negative_max_queues():
    text_message = gen_text_message()
    text_message_updated = gen_text_message()

    for queue in range(100):
        post_data(text_message=text_message, queue=queue)

    post_data(text_message=text_message, queue=101)

    for queue in range(100):
        assert put_data(text_message=text_message_updated, queue=queue).status_code == 500

    put_data(text_message=text_message_updated, queue=101)

    for queue in range(100):
        assert get_data(queue=queue).json()['message'] == text_message_updated

    assert get_data(queue=101).status_code == 404


def test_put_positive_message_limit():
    text_message = gen_text_message()
    text_message_updated = gen_text_message()

    for _ in range(100):
        post_data(text_message=text_message)

    for _ in range(100):
        assert put_data(text_message=text_message_updated).status_code == 500

    for _ in range(100):
        assert get_data().json()['message'] == text_message_updated


@pytest.mark.parametrize('boundary', [0, 1, 9999, 10001])
def test_put_positive_boundary(boundary):
    text_message = gen_text_message()
    text_message_updated = gen_text_message()

    post_data(text_message=text_message, queue=boundary)
    assert put_data(text_message=text_message_updated, queue=boundary).status_code == 500
    assert get_data(queue=boundary).json()['message'] == text_message_updated


@pytest.mark.parametrize('negative_boundary', [-1, 10001])
def test_delete_negative_boundary(negative_boundary):
    text_message = gen_text_message()
    text_message_updated = gen_text_message()

    post_data(text_message=text_message, queue=negative_boundary)
    assert put_data(text_message=text_message_updated, queue=negative_boundary).status_code == 400
    assert get_data(queue=negative_boundary).json()['message'] != text_message_updated
