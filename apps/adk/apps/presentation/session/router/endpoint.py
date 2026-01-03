from fastapi import APIRouter, Depends

from apps.applications.session.usecases.create_session import (
    CreateSessionCommand,
    CreateSessionUseCase,
)
from apps.applications.session.usecases.delete_session import DeleteSessionCommand, DeleteSessionUseCase
from apps.applications.session.usecases.reconnect_session import (
    ReconnectSessionQuery,
    ReconnectSessionUseCase,
)
from apps.presentation.dependency import (
    get_app_name,
    get_create_session_uc,
    get_delete_session_uc,
    get_reconnect_session_uc,
)
from apps.presentation.session.schemas.sessions import (
    CreateSessionRequest,
    CreateSessionResponse,
    DeleteSessionRequest,
    DeleteSessionResponse,
    SessionInfoResponse,
)

router = APIRouter()


@router.post("", response_model=CreateSessionResponse)
async def create_session(
    agent_id: str,
    req: CreateSessionRequest,
    app_name: str = Depends(get_app_name),
    uc: CreateSessionUseCase = Depends(get_create_session_uc),
):
    """
    2) chat 시작을 위한 Session 생성
    - session_id를 안 주면 서버에서 UUID로 생성
    """
    result = await uc.execute(
        CreateSessionCommand(
            user_id=req.user_id,
            session_id=req.session_id
        )
    )
    return CreateSessionResponse(
        app_name=app_name,
        user_id=result.user_id,
        session_id=result.session_id
    )

@router.get("/{user_id}/{session_id}", response_model=SessionInfoResponse)
async def reconnect_session(
    user_id: str,
    session_id: str,
    app_name: str = Depends(get_app_name),
    uc: ReconnectSessionUseCase = Depends(get_reconnect_session_uc),
):
    """
    3) Session 재연결
    - 세션이 존재하는지만 확인하고,
      이후 동일한 user_id/session_id로 /chat을 계속 호출하면 됩니다.
    """
    result = await uc.execute(
        ReconnectSessionQuery(
            user_id=user_id,
            session_id=session_id
        )
    )
    return SessionInfoResponse(
        exists=result.exists,
        app_name=app_name,
        user_id=result.user_id,
        session_id=result.session_id,
    )

@router.delete("", response_model=DeleteSessionResponse)
async def delete_session(
    req: DeleteSessionRequest,
    uc: DeleteSessionUseCase = Depends(get_delete_session_uc),
):
    result = await uc.execute(
        DeleteSessionCommand(
            app_name=req.app_name,
            user_id=req.user_id,
            session_id=req.session_id
        )
    )
    return DeleteSessionResponse(
        app_name=result.app_name,
        user_id=result.user_id,
        session_id=result.session_id
    )
