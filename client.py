from warnings import simplefilter
import requests
from json import dumps
import logging
import urllib3
import config

logging.basicConfig(filename='/Users/phavry/Desktop/logfile',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

simplefilter(
    'ignore',
    urllib3.exceptions.InsecureRequestWarning,
)


def post_data(text_message, queue=None, **kwargs):
    message_dict = {"message": text_message}
    if queue is None:
        param = dumps(message_dict)
    else:
        message_dict.update({"queue": queue})
        param = dumps(message_dict)
    response = requests.post(url=f'{config.url}:{config.port}',
                             json=param, **kwargs)
    return response


def get_data(queue=None, **kwargs):
    if queue is None:
        param = {}
    else:
        param = {'queue': queue}
    response = requests.get(url=f'{config.url}:{config.port}',
                            params=param, **kwargs)
    return response


def put_data(text_message, queue=None, **kwargs):
    message_dict = {"message": text_message}
    if queue is None:
        param = dumps(message_dict)
    else:
        message_dict.update({"queue": queue})
        param = dumps(message_dict)
    response = requests.put(url=f'{config.url}:{config.port}',
                            data=param, **kwargs)
    return response


def delete_data(queue=None, **kwargs):
    if queue is None:
        param = {}
    else:
        param = {'queue': queue}
    response = requests.delete(url=f'{config.url}:{config.port}',
                               params=param, **kwargs)
    return response
