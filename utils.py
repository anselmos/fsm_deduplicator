import logging
import logging.config
import pickle
from datetime import datetime
from os import path, walk

import redis

from constants import REDIS_HOST, REDIS_PASSWORD


def get_logger_config(name=None):
    logging.config.fileConfig('logging.conf', defaults={
        "log_date": datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    })
    return logging.getLogger(name)

def enumerate_files(init_path=None):
    if not init_path:
        raise ValueError("No init_path provided - or not available at .env")
    for (root, dirnames, filenames) in walk(init_path):
        for filename in filenames:
            yield path.join(root, filename)


def get_paths_redis():
    return redis.Redis(
        host=REDIS_HOST, port=30036, password=REDIS_PASSWORD,
        decode_responses=True, db=0)


# def save_pickle
def load_pickle(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)

def save_pickle(filename, object):
    with open(filename, "wb") as f:
        pickle.dump(object, f)