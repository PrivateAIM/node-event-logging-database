from pydantic import BaseModel, ConfigDict


class AttributesModel(BaseModel):
    """Base class that should be used as a parent class to define additional attributes for specific event types."""

    model_config = ConfigDict(extra="forbid")


class EventModelMap:
    """A simple class that implements a mapping between event names and their corresponding Pydantic models to validate
    them.

    Attributes
    ----------
    mapping : dict[str, type[AttributesModel]]
        A dictionary that maps event names to AttributesModel classes.

    Notes
    -----
    If there is no model defined in mapping for a certain event type, AttributesModel is used per default for
    validation. Since there are no attributes defined in AttributesModel and extra attributes are forbidden, a
    ValidationError is thrown as soon as the attributes dictionary is not empty.
    """

    mapping: dict[str, type[AttributesModel]] = {}

    def __call__(self, event_name: str) -> type[AttributesModel]:
        return self.mapping.get(event_name, AttributesModel)
