import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv('DB_URL', 'sqlite:///db.sqlite')
DB_ECHO = bool(os.getenv('DB_ECHO', False))
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
