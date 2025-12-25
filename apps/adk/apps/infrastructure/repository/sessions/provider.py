from google.adk.sessions import DatabaseSessionService

from apps.infrastructure.database.config.postgres import PostgresSettings, build_postgres_dsn, build_postgres_dsn_sync


class SessionProvider:
    """ """

    def __init__(self, config: PostgresSettings) -> None:
        self._config = config

    def __call__(self) -> DatabaseSessionService:
        return DatabaseSessionService(
            build_postgres_dsn(),
            # connect_args={"options": f"-c search_path={self._config.schema}"},
            connect_args={"server_settings": {"search_path": self._config.schema}},
        )

    # def build_session_service() -> DatabaseSessionService:
    #     return DatabaseSessionService(
    #         build_postgres_dsn_sync(),
    #         # execution_options={"schema_translate_map": {None, service.schema}}
    #         connect_args={"options": f"-c search_path={service.schema}"},
    #     )
