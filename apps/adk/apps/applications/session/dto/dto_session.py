from dataclasses import dataclass


@dataclass(frozen=True)
class CreateSessionCommand:
    # agent_id: str
    user_id: str

@dataclass(frozen=True)
class DeleteSessionCommand:
    # agent_id: str
    user_id: str
    session_id: str

@dataclass(frozen=True)
class GetSessionInfoQuery:
    # agent_id: str
    user_id: str
    session_id: str

@dataclass
class SessionInfoResult:
    # agent_id: str
    app_name: str
    user_id: str
    session_id: str
    state: dict
    exists: bool = False
