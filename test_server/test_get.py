import pytest
from client import post_data, get_data
from tools import gen_text_message, gen_queue


@pytest.mark.parametrize('both_queue_type', [None, gen_queue()])
def test_get_positive_both_queue_type(both_queue_type):
    text_message = gen_text_message()

    post_data(text_message=text_message, queue=both_queue_type)
    get_entity = get_data(queue=both_queue_type)

    assert get_entity.status_code == 200
    assert get_entity.json()['message'] == text_message


def test_get_positive_delete_message():
    text_message = gen_text_message()
    queue = gen_queue()

    post_data(text_message=text_message, queue=queue)
    get_entity = get_data(queue=queue)
    assert get_entity.status_code == 200
    assert get_entity.json()['message'] == text_message
    assert get_data(queue=queue).json()['message'] == 'no messages'


def test_get_positive_empty_queue():
    queue = gen_queue()

    get_entity = get_data(queue=queue)
    assert get_entity.status_code == 200
    assert get_entity.json()['message'] == 'no messages'


@pytest.mark.parametrize('boundary', [0, 1, 9999, 10000])
def test_get_positive_boundary_condition(boundary):
    text_message = gen_text_message()

    post_data(text_message=text_message, queue=boundary)

    get_entity = get_data(queue=boundary)
    assert get_entity.status_code == 200
    assert get_entity.json()['message'] == text_message


@pytest.mark.parametrize('negative_boundary', [-1, 10001])
def test_get_negative_boundary_condition(negative_boundary):
    text_message = gen_text_message()

    post_data(text_message=text_message, queue=negative_boundary)

    get_entity = get_data(queue=negative_boundary)
    assert get_entity.status_code == 400
    assert get_entity.reason == 'Unsupported alias'


def test_get_positive_max_queues():
    text_message = gen_text_message()

    for queue in range(100):
        post_data(text_message=text_message, queue=queue)

    post_data(text_message=text_message, queue=101)

    for queue in range(100):
        get_entity = get_data(queue=queue)
        assert get_entity.status_code == 200
        assert get_entity.json()['message'] == text_message

    assert get_data(queue=101).json()['message'] == 'no messages'


def test_get_positive_message_limit():
    text_message = gen_text_message()

    for _ in range(100):
        post_data(text_message=text_message)

    for _ in range(100):
        get_entity = get_data()
        assert get_entity.status_code == 200
        assert get_entity.json()['message'] == text_message


def test_get_negative_message_limit():
    queue = gen_queue()
    text_message_in_range = gen_text_message()
    text_message_out_of_range = gen_text_message()

    for _ in range(100):
        post_data(text_message=text_message_in_range, queue=queue)

    post_data(text_message=text_message_out_of_range, queue=queue)

    get_entity = get_data(queue=queue)

    assert get_entity.status_code == 200
    assert get_entity.json()['message'] == text_message_in_range


def test_get_positive_only_one_queue_updated():
    text_message = gen_text_message()
    # ?
    for queue in range(100):
        post_data(text_message=text_message, queue=queue)

    get_data()

    get_entity = get_data()
    assert get_entity.status_code == 200
    assert get_entity.json()['message'] == 'no messages'
