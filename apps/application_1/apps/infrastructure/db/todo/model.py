from __future__ import annotations
from pydantic import BaseModel, ConfigDict
from typing import Any, List


def my_schema_extra(schema: dict[str, Any]) -> None:
    for prop in schema.get('properties', {}).values():
        prop.pop('title', None)


class TodoItem(BaseModel):
    item: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "item": "Read the next chapter of the book"
            }
        }
    )


class TodoItems(BaseModel):
    todos: List[TodoItem]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "todos": [
                    {
                        "item": "Example Schema Item 1"
                    },
                    {
                        "item": "Example Schema Item 2"
                    }
                ]
            }
        }
    )


class Todo(BaseModel):
    id: int
    item: str

    model_config = ConfigDict(
        json_schema_extra=my_schema_extra
    )
