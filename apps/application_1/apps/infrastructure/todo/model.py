from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict


def my_schema_extra(schema: dict[str, Any]) -> None:
    for prop in schema.get("properties", {}).values():
        prop.pop("title", None)


class TodoItem(BaseModel):
    item: str

    model_config = ConfigDict(json_schema_extra={"example": {"item": "Read the next chapter of the book"}})


class TodoItems(BaseModel):
    todos: list[TodoItem]

    model_config = ConfigDict(
        json_schema_extra={"example": {"todos": [{"item": "Example Schema Item 1"}, {"item": "Example Schema Item 2"}]}}
    )


class Todo(BaseModel):
    id: int
    item: str

    model_config = ConfigDict(json_schema_extra=my_schema_extra)
