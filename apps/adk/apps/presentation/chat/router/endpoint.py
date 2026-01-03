
from fastapi import APIRouter, Depends, HTTPException

from apps.applications.chat.usecases.chat import ChatCommand, ChatUseCase
from apps.applications.session.ports.adk_gateway import AdkGateway
from apps.presentation.chat.schemas.chat import ChatRequest, ChatResponse
from apps.presentation.dependency import get_chat_uc, get_gateway

router = APIRouter()


@router.post("", response_model=ChatResponse)
async def chat(
    req: ChatRequest,
    uc: ChatUseCase = Depends(get_chat_uc),
    gateway: AdkGateway = Depends(get_gateway),
):
    """
    2) 실제 채팅
    - Runner.run_async()로 이벤트 스트림을 받고,
      event.is_final_response()인 이벤트에서 최종 답변을 추출합니다.
    """
    # 세션 없으면 404 (정책을 Presentation에서 정함)
    if not await gateway.session_exists(req.user_id, req.session_id):
        raise HTTPException(status_code=404, detail="Session not found. Create session first.")

    result = await uc.execute(ChatCommand(user_id=req.user_id, session_id=req.session_id, message=req.message))
    return ChatResponse(session_id=result.session_id, reply=result.reply)
