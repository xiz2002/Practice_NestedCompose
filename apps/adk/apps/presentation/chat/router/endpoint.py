
import json

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from apps.applications.session.ports.adk_gateway import AdkGateway
from apps.applications.session.usecases.chat import ChatCommand, ChatUseCase
from apps.presentation.chat.schemas.chat import ChatRequest, ChatResponse
from apps.presentation.dependency import get_chat_uc, get_gateway

router = APIRouter()

def create_req_ctx(req: ChatRequest, session_id: str):
    return ChatCommand(
        session_id=session_id,
        user_id=req.user_id,
        message=req.message,
        is_sse=req.is_sse
    )


@router.post("", response_model=ChatResponse)
async def chat(
    cmd: ChatCommand = Depends(create_req_ctx),
    uc: ChatUseCase = Depends(get_chat_uc),
    gateway: AdkGateway = Depends(get_gateway),
):
    """
    2) 실제 채팅
    - Runner.run_async()로 이벤트 스트림을 받고,
      event.is_final_response()인 이벤트에서 최종 답변을 추출합니다.
    """
    # 세션 없으면 404 (정책을 Presentation에서 정함)
    if not await gateway.session_exists(cmd.user_id, cmd.session_id):
        raise HTTPException(status_code=404, detail="Session not found. Create session first.")

    result = await uc.execute(cmd)
    return ChatResponse(reply=result.reply)


def to_sse(data: dict, event_name: str | None = None) -> str:
    # event: <name>은 선택
    lines = []
    if event_name:
        lines.append(f"event: {event_name}")
    lines.append(f"data: {json.dumps(data, ensure_ascii=False)}")
    return "\n".join(lines) + "\n\n"


@router.post(":sse")
async def chat_sse(
    cmd: ChatCommand = Depends(create_req_ctx),
    uc: ChatUseCase = Depends(get_chat_uc),
    gateway: AdkGateway = Depends(get_gateway),
):
    """
    2) 실제 채팅
    - Runner.run_async()로 이벤트 스트림을 받고,
      event.is_final_response()인 이벤트에서 최종 답변을 추출합니다.
    """
    # 세션 없으면 404 (정책을 Presentation에서 정함)
    if not await gateway.session_exists(cmd.user_id, cmd.session_id):
        raise HTTPException(status_code=404, detail="Session not found. Create session first.")

    async def gen():
        async for e in uc.execute_sse(cmd):
            yield to_sse(e)

    return StreamingResponse(
        gen(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )
