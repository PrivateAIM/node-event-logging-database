import importlib.metadata


__version__ = importlib.metadata.version("node-event-logging-database")
__version_info__ = tuple(int(token) for token in __version__.split("."))
