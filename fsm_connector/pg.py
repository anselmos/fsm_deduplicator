

from fsm_connector.base import BaseConnector
from fsm_connector.db.models import Base, File, Image
from constants import DB_URL, DB_ECHO
from utils import get_logger_config

logger = get_logger_config(__name__)

class PGConnector(BaseConnector):
    def create_db(self):
        """
        Should only be invokes at initialization
        """
        File.metadata.create_all(self.engine)
        Image.metadata.create_all(self.engine)

    def add(self, data):
        super().add(data)
        logger.debug(f"pg-add : {data}")
        with self.get_session() as session:
            session.add(File(**data))
            session.commit()
            session.close()

    def add_in_batch(self, data_list):
        with self.get_session() as session:
            logger.debug(data_list)
            session.add_all([File(**element) for element in data_list])
            session.commit()
            session.close()
