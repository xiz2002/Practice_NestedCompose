from fastapi import APIRouter, Path, HTTPException, status
from apps.infrastructure.todo.model import Todo, TodoItem, TodoItems

router = APIRouter()

todo_list = []


@router.post("/todo")
async def add_todo(item: Todo) -> dict:
    todo_list.append(item)
    return {
        "message": "Todo added successfully",
    }


# @router.get("/todo", response_model=TodoItems)
# async def retrieve_todo() -> dict:
#     return {
#         "todos": todo_list
#     }


@router.get("/todo/{todo_id}")
async def retrieve_todo(todo_id: int = Path(..., title="The ID of the todo to retrieve.")) -> Todo | dict:
    for todo in todo_list:
        if todo.id == todo_id:
            return {
                "todo": todo
            }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Todo with supplied ID does not exist.")


@router.put("/todo/{todo_id}")
async def update_todo(todo_data: TodoItem, todo_id: int = Path(..., title="The ID of the todo to update.")) -> dict:
    for index, todo in enumerate(todo_list):
        if todo.id == todo_id:
            todo.item = todo_data.item
            # updated_todo = Todo(id=todo.id, item=todo_data)
            # todo_list[index] = updated_todo
            return {
                "message": "Todo updated successfully",
            }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Todo with supplied ID does not exist.")


@router.delete("/todo/{todo_id}")
async def delete_todo(todo_id: int = Path(..., title="The ID of the todo to delete.")) -> dict:
    for index, todo in enumerate(todo_list):
        if todo.id == todo_id:
            todo_list.pop(index)
            return {
                "message": "Todo deleted successfully",
            }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Todo with supplied ID does not exist.")


@router.delete("/todo")
async def delete_all_todo() -> dict:
    todo_list.clear()
    return {
        "message": "All Todo items deleted successfully",
    }
