import peewee as pw
import pytest

from tests.common.env import postgres_user, postgres_database, postgres_password, postgres_host, postgres_port


@pytest.fixture(scope="package")
def postgres():
    return pw.PostgresqlDatabase(
        postgres_database(),
        user=postgres_user(),
        password=postgres_password(),
        host=postgres_host(),
        port=postgres_port(),
    )
