# FastAPI Google ADK SQLAlchemy App

간단한 FastAPI 기반 프로젝트 템플릿입니다. 이 레포는 `apps` 디렉터리를 패키지 루트로 사용하며, `apps.presentation.api:app`을 Uvicorn으로 실행할 수 있습니다.

**주요 기술 스택**

- FastAPI
- SQLAlchemy
- Alembic (마이그레이션)
- Uvicorn
- Pydantic

**요구사항**

- Python 3.10 이상

## 설치 및 실행 환경

1. 가상환경 생성 및 활성화

```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

2. 패키지 설치 (개발 중에는 editable 설치 권장)

```
pip install -e .
```

3. (선택) 개발 도구

```
pip install ruff
```

4. (주의) Windows환경의 WSL인 경우.
다음의 WSL 내부에 프로젝트 파일을 옮겨서 실행하지 않으면 IO병목으로 느려집니다.
```
\\WSL\{$WSL_Name}\home\{$User}\workspaces
```

## 데이터베이스 설정 / 마이그레이션

Alembic 설정 파일(`alembic.ini`)에 `sqlalchemy.url` 항목이 기본값(`driver://user:pass@localhost/dbname`)으로 되어 있습니다. 실제 DB 정보를 입력한 뒤 마이그레이션을 실행하세요.

예시(Postgres + asyncpg):

```
# alembic.ini의 sqlalchemy.url을 편집하거나 아래처럼 교체
sed -i "s|driver://user:pass@localhost/dbname|postgresql+asyncpg://myuser:mypass@localhost:5432/mydb|" alembic.ini

alembic -c alembic.ini upgrade head
```

주의: `migrations/env.py`는 `alembic.ini`의 `sqlalchemy.url` 항목을 사용합니다.

## 애플리케이션 실행

로컬 개발 서버 실행 명령 예시:

```
uvicorn apps.presentation.api:app --reload --host 0.0.0.0 --port 8000
```

웹 브라우저에서 http://127.0.0.1:8000/ 에 접속하면 환영 메시지를 확인할 수 있습니다.

## API 예시

`apps.presentation.todo`에 간단한 라우터가 있습니다. `TodoItem` 모델은 `apps.infrastructure.db.todo.model.TodoItem`에 정의되어 있습니다.

샘플 POST (새 라우트 추가):

```
curl -X POST "http://127.0.0.1:8000/api/presentation/route" \
  -H "Content-Type: application/json" \
  -d '{"id":1,"item":"buy milk"}'
```

샘플 GET (추가된 라우트 목록 조회):

```
curl http://127.0.0.1:8000/api/presentation/route
```

응답 예시(JSON):

```
{
  "routes": [
    {"id": 1, "item": "buy milk"}
  ]
}
```

## 프로젝트 구조 (핵심)

- `apps/` : 실제 패키지 코드 (패키지 루트로 설정됨)
  - `presentation/` : FastAPI 라우터 (`api.py`, `todo.py` 등)
  - `infrastructure/db/todo/model.py` : Pydantic 모델 정의
- `migrations/` : Alembic 마이그레이션 스크립트
- `alembic.ini` : Alembic 구성
- `pyproject.toml` : 프로젝트 메타 및 의존성

## 개발 팁

- 코드 스타일 검사: `ruff .` 또는 `ruff check --fix .` (pyproject에 설정 있음)
- 패키지 변경시 `pip install -e .`로 재설치 필요 없음 (editable 설치 권장)

## 추가 안내

- DB 연결 문자열, 포트, 호스트 등은 환경에 맞게 조정하세요.
- CI/CD나 배포 환경에서는 `uvicorn` 대신 `gunicorn` + `uvicorn.workers.UvicornWorker` 같은 프로덕션 서버 사용을 권장합니다.

궁금한 점이나 추가로 넣고 싶은 실행 예제가 있으면 알려주세요.
