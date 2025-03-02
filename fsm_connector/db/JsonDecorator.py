import json
from sqlalchemy import TypeDecorator, types

class JsonDecorator(TypeDecorator):
    """
    Thanks to Xiwei Wang from stackoverflow answer:
    https://stackoverflow.com/a/49933601
    Based on http://docs.sqlalchemy.org/en/latest/core/custom_types.html#sqlalchemy.types.TypeDecorator
    """

    @property
    def python_type(self):
        return object

    impl = types.String

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_literal_param(self, value, dialect):
        return value

    def process_result_value(self, value, dialect):
        try:
            return json.loads(value)
        except (ValueError, TypeError):
            return None
