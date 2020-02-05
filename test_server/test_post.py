import pytest
from client import post_data, get_data
from tools import gen_queue, gen_text_message


def test_post_positive_message_and_queue():
    text_message = gen_text_message()
    queue = gen_queue()

    post_entity = post_data(text_message=text_message, queue=queue)

    assert post_entity.status_code == 201
    assert post_entity.reason == 'Ok'
    assert get_data(queue=queue).json()['message'] == text_message


def test_post_positive_message_default_queue():
    text_message = gen_text_message()

    post_entity = post_data(text_message=text_message)

    assert post_entity.status_code == 201
    assert post_entity.reason == 'Ok'
    assert get_data().json()['message'] == text_message


def test_post_negative_empty_message_default_queue():

    post_entity = post_data(text_message='')

    assert post_entity.status_code == 400
    assert post_entity.reason == 'Message is empty'
    assert get_data().json()['message'] == 'no messages'


def test_post_negative_empty_message_with_queue():
    queue = gen_queue()

    post_entity = post_data(text_message='', queue=queue)

    assert post_entity.status_code == 400
    assert post_entity.reason == 'Message is empty'
    assert get_data(queue=queue).json()['message'] == 'no messages'


@pytest.mark.parametrize('boundary', [0, 1, 9999, 10000])
def test_post_positive_boundary_condition(boundary):
    text_message = gen_text_message()

    post_entity = post_data(text_message=text_message, queue=boundary)

    assert post_entity.status_code == 201
    assert post_entity.reason == 'Ok'
    assert get_data(queue=boundary).json()['message'] == text_message


@pytest.mark.parametrize('negative_boundary', [-1, 10001])
def test_post_negative_boundary_condition(negative_boundary):
    text_message = gen_text_message()

    post_entity = post_data(text_message=text_message, queue=negative_boundary)

    assert post_entity.status_code == 400
    assert post_entity.reason == 'Queue must be <= 10000'
    assert get_data(queue=negative_boundary).reason == 'Unsupported alias'


def test_post_positive_max_queues():
    text_message = gen_text_message()

    for queue in range(100):
        post_entity = post_data(text_message=text_message, queue=queue)
        assert post_entity.status_code == 201
        assert post_entity.reason == 'Ok'

    post_data(text_message=text_message, queue=101)

    for queue in range(100):
        assert get_data(queue=queue).json()['message'] == text_message

    assert get_data(queue=101).json()['message'] == 'no messages'


def test_post_positive_message_limit():
    text_message = gen_text_message()

    for _ in range(100):
        post_entity = post_data(text_message=text_message)
        assert post_entity.status_code == 201
        assert post_entity.reason == 'Ok'

    for _ in range(100):
        assert get_data().json()['message'] == text_message


def test_post_positive_ignore_message():
    queue = gen_queue()
    text_message_in_range = gen_text_message()
    text_message_out_of_range = gen_text_message()

    for message in range(100):
        pos_entity = post_data(text_message=text_message_in_range, queue=queue)
        assert pos_entity.status_code == 201
        assert pos_entity.reason == 'Ok'

    post_data(text_message=text_message_out_of_range, queue=queue)

    assert get_data(queue=queue).json()['message'] == text_message_in_range


def test_post_positive_only_one_queue_updated():
    text_message = gen_text_message()

    post_data(text_message=text_message)

    for queue in range(1, 100):
        assert get_data(queue=queue).json()['message'] == 'no messages'
