
from dataclasses import dataclass
from typing import Any

# @dataclass
# class Session:
#     app_name: str
#     user_id: str
#     id: str
#     state: dict
#     exists: bool

@dataclass(frozen=True)
class AppName:
    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("AppName cannot be empty")


@dataclass(frozen=True)
class UserId:
    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("UserId cannot be empty")


@dataclass(frozen=True)
class SessionId:
    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("SessionId cannot be empty")


@dataclass(frozen=True)
class State:
    value: dict[str, Any] | None
