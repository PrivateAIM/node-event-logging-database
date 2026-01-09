from contextlib import contextmanager
import datetime

import peewee as pw
from playhouse.postgres_ext import BinaryJSONField
from playhouse.shortcuts import ThreadSafeDatabaseMetadata

from .validation import EventModelMap


class BaseModel(pw.Model):
    class Meta:
        model_metadata_class = ThreadSafeDatabaseMetadata


class EventLog(BaseModel):
    # Schema is derived from OpenTelemetry's event definition.
    # https://opentelemetry.io/docs/specs/otel/logs/data-model/#log-and-event-record-definition
    """Database table schema for event logs.

    Attributes
    ----------
    event_name : str
        A name that identifies a certain type of events. This name should uniquely identify the event structure (both
        body and attributes). This attribute is not nullable. This column is indexed to improve query performance.
    service_name : str
        The name of the service that creates the event log. This is attribute is not nullable. This column is indexed to
        improve query performance.
    timestamp : datetime.datetime
        The exact timestamp when the event took place. Defaults to the point in time when the event log is created. This
        column is indexed to improve query performance.
    body : str
        A string containing the body of the event log, i.e. a human-readable string message (including multi-line).
        Defaults to an empty string.
    attributes : dict
        Additional information about the event stored in a structured way so that they can be accessed easily by the UI.
        Defaults to an empty dictionary. Dictionaries are validated by Pydantic models that are defined in the
        validation module based on the corresponding name of the event.

    Notes
    -----
    An id column is automatically created by peewee.
    """

    event_name = pw.CharField(index=True)
    service_name = pw.CharField(index=True)
    timestamp = pw.DateTimeField(default=datetime.datetime.now, index=True)
    body = pw.TextField(default=str)
    # Note that the binary JSON type only works with Postgres 9.4 or later.
    # https://docs.peewee-orm.com/en/latest/peewee/playhouse.html#json-support
    attributes = BinaryJSONField(default=dict)

    @classmethod
    def create(cls, **query):
        # Validate event attributes before persisting based on event names.
        event_name = query.get("event_name", None)
        if event_name is not None:
            model = EventModelMap()(event_name=event_name)
            attributes = query.get("attributes", {})
            if not isinstance(attributes, dict):
                raise ValueError(f"'attributes' need to be a dictionary, got {type(attributes)}.")
            model(**attributes)
        super().create(**query)


@contextmanager
def bind_to(db: pw.Database):
    with db.bind_ctx((EventLog,)):
        # Create tables if they do not exist yet.
        db.create_tables((EventLog,))
        yield
