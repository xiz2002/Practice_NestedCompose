
from google.adk.sessions.session import Session

from apps.applications.session.dto import SessionInfoResult


def _to_dto(e: Session | None, app_name: str = "") -> SessionInfoResult:
    """
    Mapper: Infastructure -> Application DTO
    Converts a ADK.Session to DTO.

    Examples:
    ```
    _to_dto(e) -> SessionInfoResult(...)
    [_to_dto(e) for e in entities] -> [SessionInfoResult(...), ...]]
    ```

    Args:
        e: ADK.Session

    Returns:
        Application DTO
    """
    if e is None:
        return SessionInfoResult(
            app_name=app_name,
            user_id="",
            session_id="",
            state={},
            exists=False
        )

    return SessionInfoResult(
        app_name=e.app_name,
        user_id=e.user_id,
        session_id=e.id,
        state=e.state,
        exists=True
    )
