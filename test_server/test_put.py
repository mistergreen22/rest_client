import pytest
from client import put_data, post_data, get_data
from tools import gen_text_message, gen_queue, gen_port


@pytest.mark.parametrize('both_queue_type', [None, gen_queue()])
def test_put_positive_both_queue_type(both_queue_type, run_stop_server_module):
    run_stop_server_module()
    text_message = gen_text_message()
    text_message_updated = gen_text_message()

    post_data(text_message=text_message, queue=both_queue_type)

    put_entity = put_data(text_message=text_message_updated,
                          queue=both_queue_type)

    assert put_entity.reason == 'No Content'
    assert put_entity.status_code == 205
    assert get_data(queue=both_queue_type
                    ).json()['message'] == text_message_updated


@pytest.mark.parametrize('both_queue_type', [None, gen_queue()])
def test_put_negative_message_and_queue(both_queue_type,
                                        run_stop_server_module):
    run_stop_server_module()
    text_message = gen_text_message()

    put_entity = put_data(text_message=text_message, queue=both_queue_type)

    assert put_entity.status_code == 404
    assert put_entity.reason == 'Not Found'


def test_put_positive_empty_message(run_stop_server_module):
    run_stop_server_module()
    text_message = gen_text_message()
    queue = gen_queue()

    post_data(text_message=text_message, queue=queue)

    put_entity = put_data(text_message='', queue=queue)

    assert put_entity.status_code == 205
    assert put_entity.reason == 'No Content'
    assert get_data(queue=queue).json()['message'] == ''


def test_put_positive_max_queues(run_stop_server_function):
    port = gen_port()
    run_stop_server_function(port=port)
    text_message = gen_text_message()
    text_message_updated = gen_text_message()

    for queue in range(100):
        post_data(text_message=text_message, queue=queue, port=port)

        put_entity = put_data(text_message=text_message_updated, queue=queue,
                              port=port)

        assert put_entity.status_code == 205
        assert put_entity.reason == 'No Content'

        assert get_data(queue=queue, port=port
                        ).json()['message'] == text_message_updated

    post_data(text_message=text_message, queue=101, port=port)

    put_entity_2 = put_data(text_message=text_message_updated, queue=101,
                            port=port)

    assert put_entity_2.status_code == 404
    assert put_entity_2.reason == 'Not Found'


def test_put_positive_message_limit(run_stop_server_module):
    port = gen_port()
    run_stop_server_module(port=port)
    text_message = gen_text_message()
    text_message_updated = gen_text_message()
    queue = gen_queue()

    for _ in range(100):
        post_data(text_message=text_message, queue=queue, port=port)

    for _ in range(100):
        put_entity = put_data(text_message=text_message_updated, queue=queue,
                              port=port)
        assert put_entity.status_code == 205
        assert put_entity.reason == 'No Content'
        assert get_data(queue=queue).json()['message'] == text_message_updated


def test_put_positive_not_updating_all_messages(run_stop_server_module):
    run_stop_server_module()
    text_message = gen_text_message()
    text_message_updated = gen_text_message()
    first_queue = gen_queue()
    second_queue = gen_queue()

    post_data(text_message=text_message, queue=first_queue)
    post_data(text_message=text_message, queue=second_queue)

    put_entity = put_data(text_message=text_message_updated, queue=first_queue)

    assert put_entity.status_code == 205
    assert put_entity.reason == 'No Content'

    assert get_data(queue=second_queue).json()['message'] == text_message
