from warnings import simplefilter
import requests
from json import dumps
import logging
import urllib3
from config import port, url, protocol
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


def post_data(text_message, queue=0, **kwargs):
    param = dumps({"message": text_message, "queue": queue})
    response = requests.post(url=f'{protocol}://{url}:{port}',
                             json=param, **kwargs)
    return response


def get_data(queue=0, **kwargs):
    param = {'queue': queue}
    response = requests.get(url=f'{protocol}://{url}:{port}',
                            params=param, **kwargs).json()['message']
    return response


def put_data(text_message, queue=0, **kwargs):
    param = dumps({"message": text_message, "queue": queue})
    response = requests.put(url=f'{protocol}://{url}:{port}',
                            data=param, **kwargs)
    return response


def delete_data(queue=0, **kwargs):
    param = {'queue': queue}
    response = requests.delete(url=f'{protocol}://{url}:{port}',
                               params=param, **kwargs)
    return response
