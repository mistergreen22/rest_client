import pytest
from client import post_data, get_data
from tools import gen_text_message, gen_queue, gen_port


@pytest.mark.parametrize('both_queue_type', [None, gen_queue()])
def test_get_positive_both_queue_type(both_queue_type, run_stop_server_module):
    run_stop_server_module()
    text_message = gen_text_message()

    post_data(text_message=text_message, queue=both_queue_type)
    get_entity = get_data(queue=both_queue_type)

    assert get_entity.status_code == 200
    assert get_entity.json()['message'] == text_message


def test_get_positive_delete_message(run_stop_server_module):
    run_stop_server_module()
    text_message = gen_text_message()
    queue = gen_queue()

    post_data(text_message=text_message, queue=queue)
    get_entity = get_data(queue=queue)
    assert get_entity.status_code == 200
    assert get_entity.json()['message'] == text_message
    assert get_data(queue=queue).json()['message'] == 'no messages'


def test_get_positive_empty_queue(run_stop_server_module):
    run_stop_server_module()
    queue = gen_queue()

    get_entity = get_data(queue=queue)
    assert get_entity.status_code == 200
    assert get_entity.json()['message'] == 'no messages'


def test_get_positive_max_queues(run_stop_server_function):
    text_message = gen_text_message()
    port = gen_port()
    run_stop_server_function(port=port)

    for queue in range(100):
        post_data(text_message=text_message, queue=queue, port=port)

    post_data(text_message=text_message, queue=101, port=port)

    for queue in range(100):
        get_entity = get_data(queue=queue, port=port)
        assert get_entity.status_code == 200
        assert get_entity.json()['message'] == text_message

    assert get_data(queue=101, port=port).json()['message'] == 'no messages'


def test_get_positive_message_limit(run_stop_server_module):
    run_stop_server_module()
    text_message = gen_text_message()

    for _ in range(100):
        post_data(text_message=text_message)

    for _ in range(100):
        get_entity = get_data()
        assert get_entity.status_code == 200
        assert get_entity.json()['message'] == text_message


def test_get_negative_message_limit(run_stop_server_module):
    run_stop_server_module()
    queue = gen_queue()
    text_message_in_range = gen_text_message()
    text_message_out_of_range = gen_text_message()

    for _ in range(100):
        post_data(text_message=text_message_in_range, queue=queue)

    post_data(text_message=text_message_out_of_range, queue=queue)

    get_entity = get_data(queue=queue)

    assert get_entity.status_code == 200
    assert get_entity.json()['message'] == text_message_in_range


def test_get_positive_only_one_queue_updated(run_stop_server_module):
    run_stop_server_module()
    text_message = gen_text_message()
    # ?
    for queue in range(100):
        post_data(text_message=text_message, queue=queue)

    get_data()

    get_entity = get_data()
    assert get_entity.status_code == 200
    assert get_entity.json()['message'] == 'no messages'
