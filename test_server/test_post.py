import pytest
from client import post_data, get_data
from tools import gen_queue, gen_text_message, gen_port


@pytest.mark.parametrize('both_queue_type', [None, gen_queue()])
def test_post_positive_message_and_queue(both_queue_type,
                                         run_stop_server_module):
    run_stop_server_module()
    text_message = gen_text_message()
    post_entity = post_data(text_message=text_message, queue=both_queue_type)

    assert post_entity.status_code == 201
    assert post_entity.reason == 'Ok'
    assert get_data(queue=both_queue_type).json()['message'] == text_message


def test_post_negative_empty_message_default_queue(run_stop_server_module):
    run_stop_server_module()
    post_entity = post_data(text_message='')

    assert post_entity.status_code == 400
    assert post_entity.reason == 'Message is empty'
    assert get_data().json()['message'] == 'no messages'


@pytest.mark.parametrize('both_queue_type', [None, gen_queue()])
def test_post_negative_empty_message_with_queue(both_queue_type,
                                                run_stop_server_module):
    run_stop_server_module()
    post_entity = post_data(text_message='', queue=both_queue_type)

    assert post_entity.status_code == 400
    assert post_entity.reason == 'Message is empty'
    assert get_data(queue=both_queue_type).json()['message'] == 'no messages'


def test_post_positive_max_queues(run_stop_server_function):
    text_message = gen_text_message()
    port = gen_port()
    run_stop_server_function(port=port)

    for queue in range(100):
        post_entity = post_data(text_message=text_message, queue=queue,
                                port=port)
        assert post_entity.status_code == 201
        assert post_entity.reason == 'Ok'

    post_data(text_message=text_message, queue=101, port=port)

    for queue in range(100):
        assert get_data(queue=queue, port=port
                        ).json()['message'] == text_message

    assert get_data(queue=101, port=port).json()['message'] == 'no messages'


def test_post_positive_message_limit(run_stop_server_module):
    run_stop_server_module()
    text_message = gen_text_message()

    for _ in range(100):
        post_entity = post_data(text_message=text_message)
        assert post_entity.status_code == 201
        assert post_entity.reason == 'Ok'

    for _ in range(100):
        assert get_data().json()['message'] == text_message


def test_post_positive_ignore_message(run_stop_server_module):
    run_stop_server_module()
    queue = gen_queue()
    text_message_in_range = gen_text_message()
    text_message_out_of_range = gen_text_message()

    for message in range(100):
        pos_entity = post_data(text_message=text_message_in_range, queue=queue)
        assert pos_entity.status_code == 201
        assert pos_entity.reason == 'Ok'

    post_data(text_message=text_message_out_of_range, queue=queue)

    assert get_data(queue=queue).json()['message'] == text_message_in_range


def test_post_positive_only_one_queue_updated(run_stop_server_module):
    run_stop_server_module()
    text_message = gen_text_message()

    post_data(text_message=text_message)

    for queue in range(1, 100):
        assert get_data(queue=queue).json()['message'] == 'no messages'
