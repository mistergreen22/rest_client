import string
from random import randint, choice


def gen_queue():
    return randint(0, 10000)


def gen_text_message():
    return ''.join(choice(string.ascii_uppercase + string.digits
                          ) for _ in range(10))


def gen_port():
    return randint(1024, 49151)
