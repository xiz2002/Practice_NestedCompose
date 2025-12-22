from __future__ import annotations

from google.adk.runners import Runner
from google.genai import types

from apps.applications.ports.adk_gateway import AdkGateway


class AdkGatewayImpl(AdkGateway):
    """
    ADK Runner + SessionService를 감싸는 Infrastructure 구현체.
    Presentation/Application은 ADK를 직접 import 하지 않음.
    """

    def __init__(self, runner: Runner) -> None:
        self._runner = runner

    @property
    def _session_service(self):
        # Runner가 들고 있는 session_service에 접근
        return self._runner.session_service

    @property
    def _app_name(self) -> str:
        return self._runner.app_name

    async def ensure_session(self, user_id: str, session_id: str) -> None:
        s = await self._session_service.get_session(
            app_name=self._app_name,
            user_id=user_id,
            session_id=session_id,
        )
        if s is None:
            await self._session_service.create_session(
                app_name=self._app_name,
                user_id=user_id,
                session_id=session_id,
            )

    async def session_exists(self, user_id: str, session_id: str) -> bool:
        s = await self._session_service.get_session(
            app_name=self._app_name,
            user_id=user_id,
            session_id=session_id,
        )
        return s is not None

    async def chat(self, user_id: str, session_id: str, message: str) -> str:
        # 세션 없으면 Application이 아니라 여기서도 막아도 되지만,
        # 예시는 Presentation에서 404 처리하도록 exists 체크를 분리함.
        user_content = types.Content(role="user", parts=[types.Part(text=message)])

        final_text = None
        async for event in self._runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=user_content,
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    text = getattr(event.content.parts[0], "text", None)
                    final_text = text if text is not None else ""
                else:
                    final_text = ""

        if final_text is None:
            # 최종 응답 이벤트를 못 받은 경우
            raise RuntimeError("No final response captured from ADK events.")

        return final_text
