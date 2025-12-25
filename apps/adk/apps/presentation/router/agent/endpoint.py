from fastapi import APIRouter, Depends

from apps.presentation.dependency import get_app_name


router = APIRouter()


@router.get("")
async def agent_info(app_name: str = Depends(get_app_name)):
    """
    Agent 조회
    # TODO: ResponseBody 생성
    """
    return {
        "app_name": app_name,
    }


# @router.post("", response_class=)
# async def set_agent(req: [ req.body()]):
#     """
#     Agent 생성
#     """
#     return {
#         "app_name": APP_NAME,
#         "agent_name": agent.name,
#         "model": MODEL_ID,
#         "session_db_url": DB_URL,
#     }
