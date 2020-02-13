import logging
import os

logfile_path = os.path.abspath("../logfile")


def return_logger():
    logging.basicConfig(filename=logfile_path,
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

    logger = logging.getLogger(__name__)
    return logger
