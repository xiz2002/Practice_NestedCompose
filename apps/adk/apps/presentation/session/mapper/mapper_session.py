"""
① Presentation → Application (Request → Command)

✔ HTTP/API 관심사 제거
✔ validation 종료 지점
"""
from fastapi import Query

from apps.applications.session.dto import (
    CreateSessionCommand,
    DeleteSessionCommand,
    GetSessionInfoQuery,
    SessionInfoResult,
)
from apps.presentation.session.schemas import CreateSessionRequest, DeleteSessionRequest, SessionInfoResponse


# ------------------------------------------
# Presentation -> Application
# ------------------------------------------
def make_create_session_to_command(req: CreateSessionRequest) -> CreateSessionCommand:
    return CreateSessionCommand(
        user_id=req.user_id,
    )

def make_delete_session_to_command(req: DeleteSessionRequest) -> DeleteSessionCommand:
    return DeleteSessionCommand(
        user_id=req.user_id,
        session_id=req.session_id,
    )

def make_exists_session_to_query(
        session_id: str,
        user_id: str = Query(...)
    ) -> GetSessionInfoQuery:
    return GetSessionInfoQuery(
        session_id=session_id,
        user_id=user_id
    )
# ------------------------------------------
# Application -> Presentation
# ------------------------------------------
def make_session_to_response(session: SessionInfoResult) -> SessionInfoResponse:
    return SessionInfoResponse(
        app_name=session.app_name,
        user_id=session.user_id,
        session_id=session.session_id,
        state=session.state,
        exists=session.exists
    )
