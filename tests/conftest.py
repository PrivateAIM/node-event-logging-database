import peewee as pw
import pytest

from node_event_logging import init_db
from tests.common.env import postgres_user, postgres_database, postgres_password, postgres_host, postgres_port


@pytest.fixture(scope="package")
def postgres():
    db = pw.PostgresqlDatabase(
        postgres_database(),
        user=postgres_user(),
        password=postgres_password(),
        host=postgres_host(),
        port=postgres_port(),
    )
    init_db(db)
    return db
