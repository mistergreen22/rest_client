import pytest
from client import post_data, delete_data, get_data
from tools import gen_text_message, gen_queue


@pytest.mark.parametrize('both_queue_type', [None, gen_queue()])
def test_delete_positive_both_queue_type(both_queue_type):
    text_message = gen_text_message()

    post_data(text_message=text_message, queue=both_queue_type)

    delete_entity = delete_data(queue=both_queue_type)

    assert delete_entity.status_code == 204
    assert delete_entity.reason == 'Ok'
    assert get_data(queue=both_queue_type).json()['message'] == 'no messages'


@pytest.mark.parametrize('both_queue_type', [None, gen_queue()])
def test_delete_negative_with_queue(both_queue_type):

    delete_entity = delete_data(queue=both_queue_type)

    assert delete_entity.status_code == 404
    assert delete_entity.reason == 'Not Found'


def test_delete_positive_max_queue():
    text_message = gen_text_message()

    for queue in range(100):
        post_data(text_message=text_message, queue=queue)
        delete_entity = delete_data(queue=queue)

        assert delete_entity.status_code == 204
        assert delete_entity.reason == 'Ok'

        assert get_data(queue=queue).json()['message'] == 'no messages'

    post_data(text_message=text_message, queue=101)
    delete_entity_2 = delete_data(queue=101)
    assert delete_entity_2.status_code == 404
    assert delete_entity_2.reason == 'Not Found'


def test_delete_positive_message_limit():
    text_message = gen_text_message()

    for _ in range(100):
        post_data(text_message=text_message)

    for _ in range(100):
        delete_entity = delete_data()
        assert delete_entity.status_code == 204
        assert delete_entity.reason == 'Ok'

    for _ in range(100):
        assert get_data().json()['message'] == 'no messages'


@pytest.mark.parametrize('boundary', [0, 1, 9999, 10000])
def test_delete_positive_boundary_condition(boundary):
    text_message = gen_text_message()

    post_data(text_message=text_message, queue=boundary)
    delete_entity = delete_data(queue=boundary)

    assert delete_entity.status_code == 204
    assert delete_entity.reason == 'Ok'

    assert get_data(queue=boundary).json()['message'] == 'no messages'


@pytest.mark.parametrize('negative_boundary', [-1, 10001])
def test_delete_negative_boundary_condition(negative_boundary):
    text_message = gen_text_message()

    post_data(text_message=text_message, queue=negative_boundary)
    delete_entity = delete_data(queue=negative_boundary)

    assert delete_entity.status_code == 400
    assert delete_entity.reason == 'Unsupported alias'

    assert get_data(queue=negative_boundary).reason == 'Unsupported alias'


def test_delete_positive_not_deleting_all_messages():
    text_message = gen_text_message()
    first_queue = gen_queue()
    second_queue = gen_queue()

    post_data(text_message=text_message, queue=first_queue)
    post_data(text_message=text_message, queue=second_queue)

    delete_first_entity = delete_data(first_queue)

    assert delete_first_entity.status_code == 204
    assert delete_first_entity.reason == 'Ok'

    assert get_data(second_queue).json()['message'] == text_message


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


def test_delete_positive_doesnt_clean_one_queue():
    text_message = gen_text_message()
    post_data(text_message=text_message)
    post_data(text_message=text_message)
    delete_data()
    assert get_data().json()['message'] == text_message
