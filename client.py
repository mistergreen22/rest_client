from warnings import simplefilter
import requests
from json import dumps
import logging
import urllib3

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


def my_decorator(func):
    def wrapper(*args, **kwargs):
        var = logger.debug(func(*args, **kwargs))
        response = func(*args, **kwargs)

        return response

    return wrapper


def post_data(url, text_message, queue=0, **kwargs):
    my_dict = {"message": text_message, "queue": queue}
    my_dict = dumps(my_dict)
    response = requests.post(url, json=my_dict, **kwargs)
    return response


def get_data(url, queue=0, **kwargs):
    param = {'queue': queue}
    response = requests.get(url, params=param, **kwargs).json()['message']
    return response


def put_data(url, text_message, queue=0, **kwargs):
    my_dict = {"message": text_message, "queue": queue}
    my_dict = dumps(my_dict)
    response = requests.put(url, data=my_dict, **kwargs)
    return response


def delete_data(url, queue=0, **kwargs):
    param = {'queue': queue}
    response = requests.delete(url, params=param, **kwargs)
    return response

