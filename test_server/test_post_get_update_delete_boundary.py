import pytest
from client import post_data, get_data, put_data, delete_data
from tools import gen_text_message, gen_port


@pytest.mark.parametrize('boundary', [0, 1, 9999, 10000])
def test_rest_scenario_positive_boundary(boundary, run_stop_server_function):
    port = gen_port()
    run_stop_server_function(port=port)
    text_message = gen_text_message()
    text_message_updated = gen_text_message()

    post_entity = post_data(text_message=text_message, queue=boundary,
                            port=port)

    assert post_entity.status_code == 201
    assert post_entity.reason == 'Ok'

    put_entity = put_data(text_message=text_message_updated, queue=boundary,
                          port=port)

    assert put_entity.status_code == 205
    assert put_entity.reason == 'No Content'

    delete_entity = delete_data(queue=boundary, port=port)
    assert delete_entity.status_code == 204
    assert delete_entity.reason == 'Ok'

    get_entity = get_data(queue=boundary, port=port)
    assert get_entity.status_code == 200
    assert get_entity.json()['message'] == 'no messages'


@pytest.mark.parametrize('boundary', [-1, 10001])
@pytest.mark.parametrize('methods', [get_data, put_data])
def test_scenario_positive_boundary(run_stop_server_function, boundary,
                                    methods):
    port = gen_port()
    run_stop_server_function(port=port)
    entity = methods(boundary, port=port)
    assert entity.status_code == 400
    assert entity.reason == 'Unsupported alias'


@pytest.mark.parametrize('boundary', [-1, 10001])
@pytest.mark.parametrize('methods', [post_data, put_data])
def test_scenario_positive_boundary_message(run_stop_server_function, boundary,
                                            methods):
    port = gen_port()
    run_stop_server_function(port=port)
    text_message = gen_text_message()
    entity = methods(text_message, boundary, port=port)
    assert entity.status_code == 400
    assert entity.reason == 'Unsupported alias'
