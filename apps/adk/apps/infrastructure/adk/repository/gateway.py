from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any

from google.adk.agents.run_config import RunConfig, StreamingMode

# from apps.domain.session.entity_session import Session
from google.genai import types

from apps.applications.session.dto import SessionInfoResult
from apps.applications.session.ports import AdkGateway
from apps.domain.agent import Agent
from apps.infrastructure.adk.mapper import _to_dto
from apps.infrastructure.adk.repository.factory import AdkFactory
from apps.infrastructure.session.services.provider import DatabaseSessionServiceEx


class AdkGatewayImpl(AdkGateway):
    """
    ADK Runner + SessionService를 감싸는 Infrastructure 구현체.
    Presentation/Application은 ADK를 직접 import 하지 않음.
    """

    def __init__(
        self,
        agent_info: Agent,
        service: DatabaseSessionServiceEx,
        factory: AdkFactory,
    ) -> None:
        self._agent_info = agent_info
        self._service = service
        self._runner = factory.build_runner(agent_info, service)

    @property
    def _app_name(self):
        return self._agent_info.name

    @property
    def _session_service(self):
        return self._service

    async def ensure_session(self, user_id: str, session_id: str, state: dict[str, Any] | None = None) -> SessionInfoResult:
        return _to_dto(
            await self._session_service.create_session(
                app_name=self._app_name,
                user_id=user_id,
                session_id=session_id,
                state=state,
            )
        )

    async def session_delete(self, user_id: str, session_id: str) -> bool:
        s = await self._session_service.get_session(
            app_name=self._app_name,
            user_id=user_id,
            session_id=session_id,
        )
        if s is not None:
            await self._session_service.delete_session(
                app_name=self._app_name,
                user_id=user_id,
                session_id=session_id
            )
            return True
        return False

    async def session_exists(self, user_id: str, session_id: str) -> SessionInfoResult:
        s = await self._session_service.get_session(
            app_name=self._app_name,
            user_id=user_id,
            session_id=session_id,
        )
        return _to_dto(s, self._app_name)

    def _extract_text(self, event) -> str:
        if getattr(event, "content", None) and getattr(event.content, "parts", None):
            # parts에서 text를 모두 이어붙이는 방식(안전 쪽)
            texts = []
            for p in event.content.parts:
                t = getattr(p, "text", None)
                if t:
                    texts.append(t)
            return "".join(texts)
        return ""

    async def chat_events(
        self,
        user_id: str,
        session_id: str,
        message: str
    ) -> str:
        # 세션 없으면 Application이 아니라 여기서도 막아도 되지만,
        # 예시는 Presentation에서 404 처리하도록 exists 체크를 분리함.
        user_content = types.Content(
            role="user",
            parts=[types.Part(text=message)]
        )

        final_text = None
        async for event in self._runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=user_content,
            run_config=None
        ):
            if event.is_final_response():
                final_text = self._extract_text(event)

        if final_text is None:
            # 최종 응답 이벤트를 못 받은 경우
            raise RuntimeError("No final response captured from ADK events.")

        return final_text

    def chat_events_sse(
        self,
        user_id: str,
        session_id: str,
        message: str
    ) -> AsyncIterator[dict[str, Any]]:
        user_content = types.Content(
            role="user",
            parts=[types.Part(text=message)]
        )

        run_config = RunConfig(
            streaming_mode=StreamingMode.SSE,
            response_modalities=["TEXT"],
        )

        async def _gen() -> AsyncIterator[dict[str, Any]]:
            async for event in self._runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=user_content,
                run_config=run_config,
            ):
                # 1) pydantic v2
                if hasattr(event, "model_dump"):
                    # JSON 안전 우선 (가능한 경우)
                    try:
                        payload = event.model_dump(mode="json")
                    except TypeError:
                        payload = event.model_dump()
                    yield payload
                    continue

                # 2) pydantic v1
                if hasattr(event, "dict"):
                    yield event.dict()
                    continue

                # 3) fallback
                yield {"event": str(event)}

        return _gen()
