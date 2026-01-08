from contextlib import contextmanager
import datetime

import peewee as pw
from playhouse.postgres_ext import BinaryJSONField
from playhouse.shortcuts import ThreadSafeDatabaseMetadata


class BaseModel(pw.Model):
    class Meta:
        model_metadata_class = ThreadSafeDatabaseMetadata


class EventLog(BaseModel):
    # Schema is derived from OpenTelemetry's event definition.
    # https://opentelemetry.io/docs/specs/otel/logs/data-model/#log-and-event-record-definition

    event_name = pw.CharField(index=True)
    service_name = pw.CharField(index=True)
    timestamp = pw.DateTimeField(default=datetime.datetime.now, index=True)
    body = pw.TextField(null=True)
    # Note that the binary JSON type only works with Postgres 9.4 or later.
    # https://docs.peewee-orm.com/en/latest/peewee/playhouse.html#json-support
    attributes = BinaryJSONField(null=True)


@contextmanager
def bind_to(db: pw.Database):
    with db.bind_ctx((EventLog,)):
        # Create tables if they do not exist yet.
        db.create_tables((EventLog,))
        yield
