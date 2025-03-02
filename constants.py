import os
from dotenv import load_dotenv

load_dotenv()

KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'fsm_file_path')
KAFKA_HOST = os.getenv('KAFKA_HOST', 'localhost')
KAFKA_PORT = os.getenv('KAFKA_PORT', '9092')
KAFKA_GROUP_ID = os.getenv('KAFKA_GROUP_ID', 'my-group')
DB_URL = os.getenv('DB_URL', 'sqlite:///db.sqlite')
DB_ECHO = bool(os.getenv('DB_ECHO', False))
PATH_CLEAN = bool(os.getenv('PATH_CLEAN', False))
INIT_PATH = os.getenv('INIT_PATH')
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
