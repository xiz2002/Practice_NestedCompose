
"""
② Application → Domain (Command → Entity)

✔ 비즈니스 모델 생성/갱신
✔ 도메인 불변성 유지

📍 이건 Application 레이어 책임
→ applications/agent/mappers
"""

# ------------------------------------------
# Application -> Domain
# ------------------------------------------
# TODO: 분리
# def make_session_entity_from_command(
#     app_name: str,
#     session_id: str,
#     exists: bool,
#     cmd: CreateSessionCommand | DeleteSessionCommand
# ) -> Session:
#     return Session(
#         app_name=app_name,
#         user_id=cmd.user_id,
#         id=session_id,
#         state={},
#         exists=exists
#     )

# ------------------------------------------
# Domain -> Application
# ------------------------------------------
# def make_session_dto_from_entity(agent_id: str, e: Session) -> SessionInfoResult:
#     return SessionInfoResult(
#         agent_id=agent_id,
#         user_id=e.user_id,
#         app_name=e.app_name,
#         session_id=e.id,
#         state=e.state,
#         exists=e.exists
#     )
