"""
Base connector for any other processor connectors
Has a `add` that is override by specific connector to add data into connector
"""
from utils import get_logger_config
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from constants import DB_URL, DB_ECHO
logger = get_logger_config(__name__)

class BaseConnector:
    def __init__(self):
        self.engine = self.get_engine()

    def get_engine(self):
        return create_engine(DB_URL, echo=DB_ECHO)

    def add(self, data):
        logger.debug(f"connector-base: {data}")

    def get_session(self):
        return Session(self.engine)

    def get_query(self, model):
        session = self.get_session()
        return session.query(model)

