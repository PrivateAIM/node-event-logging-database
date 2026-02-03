import datetime
import uuid

import pytest
from pydantic import ValidationError

from node_event_logging import AttributesModel, bind_to, EventLog, EventModelMap
from .common.helpers import next_random_string, next_uuid


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

        timestamp = datetime.datetime.now(tz=datetime.timezone.utc)
        body = next_random_string()
        EventLog.create(event_name=event_name, service_name=service_name, timestamp=timestamp, body=body)
        assert EventLog.select().count() == n_events + 1

        event = EventLog.select().where(EventLog.event_name == event_name).get()
        assert event.timestamp == timestamp
        assert event.body == body

        EventLog.delete().where(EventLog.event_name == event_name).execute()
        assert EventLog.select().count() == n_events


class AttributesModelTest(AttributesModel):
    attribute: uuid.UUID


def test_validating_attributes(monkeypatch, postgres):
    event_name = next_random_string()
    monkeypatch.setattr(EventModelMap, "mapping", {event_name: AttributesModelTest})

    with bind_to(postgres):
        with pytest.raises(ValidationError):
            EventLog.create(
                event_name=next_random_string(),
                service_name=next_random_string(),
                attributes={next_random_string(): next_random_string()},
            )
        with pytest.raises(ValidationError):
            EventLog.create(
                event_name=event_name,
                service_name=next_random_string(),
                attributes={next_random_string(): next_random_string()},
            )
        with pytest.raises(ValidationError):
            EventLog.create(
                event_name=event_name,
                service_name=next_random_string(),
                attributes={"attribute": next_random_string()},
            )
        with pytest.raises(ValidationError):
            EventLog.create(
                event_name=event_name,
                service_name=next_random_string(),
                attributes={"attribute": next_random_string(), next_random_string(): next_random_string()},
            )

        n_events = EventLog.select().count()
        EventLog.create(
            event_name=event_name,
            service_name=next_random_string(),
            attributes={"attribute": next_uuid()},
        )
        assert EventLog.select().count() == n_events + 1

        EventLog.delete().where(EventLog.event_name == event_name).execute()
        assert EventLog.select().count() == n_events
