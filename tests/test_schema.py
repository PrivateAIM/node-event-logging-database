import datetime

from node_event_logging import bind_to, EventLog
from .common.helpers import next_random_string


def test_database(postgres):
    with bind_to(postgres):
        assert EventLog.table_exists() is True


def test_columns(postgres):
    with bind_to(postgres):
        columns = [column.name for column in EventLog.select().selected_columns]
        assert columns == ["id", "event_name", "service_name", "timestamp", "body", "attributes"]


def test_create_and_delete(postgres):
    with bind_to(postgres):
        n_events = EventLog.select().count()
        event_name, service_name = next_random_string(), next_random_string()
        EventLog.create(event_name=event_name, service_name=service_name)
        assert EventLog.select().count() == n_events + 1

        event = EventLog.select().where(EventLog.event_name == event_name).get()
        assert event.service_name == service_name

        EventLog.delete().where(EventLog.event_name == event_name).execute()
        assert EventLog.select().count() == n_events

        timestamp = datetime.datetime.now()
        body = next_random_string()
        attributes = {next_random_string(): next_random_string()}
        EventLog.create(
            event_name=event_name, service_name=service_name, timestamp=timestamp, body=body, attributes=attributes
        )
        assert EventLog.select().count() == n_events + 1

        event = EventLog.select().where(EventLog.event_name == event_name).get()
        assert event.timestamp == timestamp
        assert event.body == body
        assert event.attributes == attributes

        EventLog.delete().where(EventLog.event_name == event_name).execute()
        assert EventLog.select().count() == n_events
