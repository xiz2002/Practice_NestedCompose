from fastapi import APIRouter, Depends

from apps.applications.session.usecases.create_session import (
    CreateSessionCommand,
    CreateSessionUseCase,
)
from apps.applications.session.usecases.delete_session import DeleteSessionCommand, DeleteSessionUseCase
from apps.applications.session.usecases.reconnect_session import (
    GetSessionInfoQuery,
    ReconnectSessionUseCase,
)
from apps.presentation.dependency import (
    get_create_session_uc,
    get_delete_session_uc,
    get_reconnect_session_uc,
)
from apps.presentation.session.mapper import (
    make_create_session_to_command,
    make_delete_session_to_command,
    make_exists_session_to_query,
    make_session_to_response,
)
from apps.presentation.session.schemas import (
    SessionInfoResponse,
)

router = APIRouter()


@router.post("", response_model=SessionInfoResponse)
async def create_session(
    cmd: CreateSessionCommand = Depends(make_create_session_to_command),
    uc: CreateSessionUseCase = Depends(get_create_session_uc),
):
    """
    Session 생성
    - chat 시작을 위한 Session
    - session_id를 안 주면 서버에서 UUID로 생성
    """
    result = await uc.execute(cmd)
    return make_session_to_response(result)

@router.delete("")
async def delete_session(
    cmd: DeleteSessionCommand = Depends(make_delete_session_to_command),
    uc: DeleteSessionUseCase = Depends(get_delete_session_uc),
):
    """
    Session 삭제
    - Session을 파기.
    """
    result = await uc.execute(cmd)
    return result

@router.get("/{session_id}", response_model=SessionInfoResponse)
async def reconnect_session(
    q: GetSessionInfoQuery = Depends(make_exists_session_to_query),
    uc: ReconnectSessionUseCase = Depends(get_reconnect_session_uc),
):
    """
    Session 재연결
    - 세션이 존재하는지만 확인하고,
      이후 동일한 user_id/session_id로 /chat을 계속 호출하면 됩니다.
    """
    result = await uc.execute(q)
    return make_session_to_response(result)
