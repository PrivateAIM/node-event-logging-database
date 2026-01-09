from pydantic import BaseModel, ConfigDict


class AttributesModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class EventModelMap:
    mapping: dict[str, type[AttributesModel]] = {}

    def __call__(self, event_name: str) -> type[AttributesModel]:
        return self.mapping.get(event_name, AttributesModel)
