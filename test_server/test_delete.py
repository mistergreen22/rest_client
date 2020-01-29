import pytest
from client import post_data, delete_data, get_data
from tools import gen_text_message, gen_queue


def test_delete_positive_with_queue():
    text_message = gen_text_message()
    queue = gen_queue()

    post_data(text_message=text_message, queue=queue)
    assert delete_data(queue=queue).status_code == 204
    assert get_data(queue=queue).json()['message'] == 'no messages'


def test_delete_positive_without_queue():
    text_message = gen_text_message()
    post_data(text_message=text_message)

    assert delete_data().status_code == 204
    assert get_data().json()['message'] == 'no messages'


def test_delete_negative_with_queue():
    queue = gen_queue()

    assert delete_data(queue=queue).status_code == 404


def test_delete_negative_without_queue():
    assert delete_data().status_code == 404


def test_delete_positive_max_queue():
    text_message = gen_text_message()

    for queue in range(100):
        post_data(text_message=text_message, queue=queue)

    for queue in range(100):
        assert delete_data(queue=queue).status_code == 204

    for queue in range(100):
        assert get_data(queue=queue).json()['message'] == 'no messages'


def test_delete_negative_max_queue():
    text_message = gen_text_message()

    for queue in range(100):
        post_data(text_message=text_message, queue=queue)

    post_data(text_message=text_message, queue=101)

    for queue in range(100):
        assert delete_data(queue=queue).status_code == 204

    for queue in range(100):
        assert get_data(queue=queue).json()['message'] == 'no messages'

    assert delete_data(queue=101).status_code == 404


def test_delete_positive_message_limit():
    text_message = gen_text_message()

    for _ in range(100):
        post_data(text_message=text_message)

    for _ in range(100):
        assert delete_data().status_code == 204

    for _ in range(100):
        assert get_data().json()['message'] == 'no messages'


@pytest.mark.parametrize('boundary', [0, 1, 9999, 10000])
def test_delete_positive_boundary_condition(boundary):
    text_message = gen_text_message()

    post_data(text_message=text_message, queue=boundary)
    assert delete_data(queue=boundary).status_code == 204
    assert get_data(queue=boundary).json()['message'] == 'no messages'


@pytest.mark.parametrize('negative_boundary', [-1, 10001])
def test_delete_negative_boundary_condition(negative_boundary):
    text_message = gen_text_message()

    post_data(text_message=text_message, queue=negative_boundary)
    assert delete_data(queue=negative_boundary).status_code == 400
    assert get_data(queue=negative_boundary).json()['message'] != text_message


def test_delete_positive_not_deleting_all_messages():
    text_message = gen_text_message()

    for queue in range(100):
        post_data(text_message=text_message, queue=queue)

    delete_data()

    for queue in range(1, 100):
        assert get_data(queue=queue).json()['message'] == text_message


def test_delete_positive_not_delete_queue():
    text_message = gen_text_message()
    queue = gen_queue()

    for _ in range(100):
        post_data(text_message=text_message, queue=queue)

    for _ in range(100):
        delete_data(queue=queue)

    delete_data(queue=queue)

    for all_queues in range(100):
        post_data(text_message=text_message, queue=all_queues)

    for all_queues in range(100):
        assert get_data(queue=all_queues).json()['message'] == text_message
