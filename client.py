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


def post_data(url, text_message, queue=0, **kwargs):
    param = dumps({"message": text_message, "queue": queue})
    response = requests.post(url, json=param, **kwargs)
    return response


def get_data(url, queue=0, **kwargs):
    param = {'queue': queue}
    response = requests.get(url, params=param, **kwargs).json()['message']
    return response


def put_data(url, text_message, queue=0, **kwargs):
    param = dumps({"message": text_message, "queue": queue})
    response = requests.put(url, data=param, **kwargs)
    return response


def delete_data(url, queue=0, **kwargs):
    param = {'queue': queue}
    response = requests.delete(url, params=param, **kwargs)
    return response

