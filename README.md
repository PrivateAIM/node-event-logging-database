# Event Logging Database Schema for Nodes

This repository provides the database schema node services use to store events so that the node UI can display them. The
schema is defined with the help of a simple and small ORM called [peewee](https://docs.peewee-orm.com/).


## Installation

```
pip install git+https://github.com/PrivateAIM/node-event-logging-database.git@v0.1.2
```


## Usage

```python
import peewee as pw
from node_event_logging import bind_to, EventLog

postgres = pw.PostgresqlDatabase("my_database", user="...", password="...", host="...", port="...")
with bind_to(postgres):
    EventLog.create(event_name="test_event", service_name="random_service")
```

For more information, read the docstring of the `EventLog` model.


## Testing

To run tests against the database schema, update the `.env.test` file if you already have a PostgreSQL instance running
or start a new one by executing `docker compose up -d` inside the repository directory. Run all tests by executing
`pytest tests`.
