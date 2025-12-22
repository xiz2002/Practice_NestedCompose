from dataclasses import dataclass


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
