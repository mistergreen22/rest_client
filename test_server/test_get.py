import pytest
from client import post_data, get_data
from tools import gen_text_message, gen_queue


def test_get_positive_message_and_queue():
    text_message = gen_text_message()
    queue = gen_queue()

    post_data(text_message=text_message, queue=queue)
    assert get_data(queue=queue).status_code == 200
    post_data(text_message=text_message, queue=queue)
    assert get_data(queue=queue).json()['message'] == text_message


def test_get_positive_message_without_queue():
    text_message = gen_text_message()

    post_data(text_message=text_message)
    assert get_data().status_code == 200
    post_data(text_message=text_message)
    assert get_data().json()['message'] == text_message


def test_get_positive_delete_message():
    text_message = gen_text_message()
    queue = gen_queue()

    post_data(text_message=text_message, queue=queue)
    assert get_data(queue=queue).json()['message'] == text_message
    assert get_data(queue=queue).json()['message'] == 'no messages'


def test_get_positive_empty_queue():
    queue = gen_queue()

    assert get_data(queue=queue).json()['message'] == 'no messages'


@pytest.mark.parametrize('boundary', [0, 1, 9999, 10000])
def test_get_positive_boundary_condition(boundary):
    text_message = gen_text_message()

    post_data(text_message=text_message, queue=boundary)
    assert get_data(queue=boundary).json()['message'] == text_message


@pytest.mark.parametrize('negative_boundary', [-1, 10001])
def test_get_negative_boundary_condition(negative_boundary):
    text_message = gen_text_message()

    post_data(text_message=text_message, queue=negative_boundary)
    assert get_data(queue=negative_boundary).json()['message'] != text_message


def test_get_positive_max_queues():
    text_message = gen_text_message()

    for queue in range(100):
        post_data(text_message=text_message, queue=queue)

    post_data(text_message=text_message, queue=101)

    for queue in range(100):
        assert get_data(queue=queue).json()['message'] == text_message

    assert get_data(queue=101).json()['message'] == 'no messages'


def test_get_positive_message_limit():
    text_message = gen_text_message()

    for _ in range(100):
        post_data(text_message=text_message)

    for _ in range(100):
        assert get_data().json()['message'] == text_message


def test_get_negative_message_limit():
    queue = gen_queue()
    text_message_in_range = gen_text_message()
    text_message_out_of_range = gen_text_message()

    for _ in range(100):
        post_data(text_message=text_message_in_range, queue=queue)

    post_data(text_message=text_message_out_of_range, queue=queue)

    assert get_data(queue=queue).json()['message'] == text_message_in_range
