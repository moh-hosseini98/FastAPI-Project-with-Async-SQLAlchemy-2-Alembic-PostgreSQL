from datetime import datetime
from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession


from core.db import get_session
from services.todo_service import TodotService
from models.todos import Todo
from schemas.todo_schema import TodoCreate,TodoUpdate,TodoRead

router = APIRouter()
todo_service = TodotService()

@router.get(
    "/",
    response_model=list[TodoRead],
    status_code=status.HTTP_200_OK,
)
async def read_todos(
    session : AsyncSession = Depends(get_session)
):
    todos = await todo_service.read_todos(session)
    return todos

@router.post(
    "/",
    response_model=TodoRead,
    status_code=status.HTTP_201_CREATED
)
async def create_todo(
    todo_data : TodoCreate,
    session : AsyncSession = Depends(get_session)
):
    new_todo = await todo_service.create_todo(todo_data,session)
    return new_todo

@router.get(
    "/{todo_id}",
    response_model=TodoRead,
    status_code=status.HTTP_200_OK
)
async def read_todo(
    todo_id : int,
    session : AsyncSession = Depends(get_session)
):
    todo = await todo_service.read_todo(todo_id,session)
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return todo    


@router.patch(
    "/{todo_id}",
    response_model=TodoRead
)
async def update_todo(
    update_data : TodoUpdate,
    todo_id : int,
    session : AsyncSession = Depends(get_session)
):
    todo = await todo_service.update_todo(
        update_data,
        todo_id,
        session
    )
    return todo


@router.delete(
    "/{todo_id}"
)
async def delete_todo(
    todo_id : int,
    session : AsyncSession = Depends(get_session)
):
    todo = await todo_service.delete_todo(todo_id,session)
    return {"message": "Todo deleted from the database"}


