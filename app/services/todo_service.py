from pydantic import EmailStr
from fastapi import APIRouter,Depends,HTTPException,status
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


from models.todos import Todo
from schemas.todo_schema import TodoCreate,TodoUpdate





class TodotService:
    async def create_todo(
        self,
        todo_data:TodoCreate,
        session:AsyncSession
    ):
        todo_data_dict = todo_data.model_dump()
        new_todo = Todo(**todo_data_dict)
        session.add(new_todo)
        await session.commit()

        return new_todo

    async def read_todos(
        self,
        session:AsyncSession
    ):
        stmt = select(Todo).order_by(Todo.created_at.desc())
        result = await session.execute(stmt)
        return result.scalars().all()

    async def read_todo(
        self,
        todo_id : int,
        session:AsyncSession
    ):
        stmt = select(Todo).where(Todo.id == todo_id)
        result = await session.execute(stmt)
        return result.scalars().first()

        return True if result is not None else None

    async def update_todo(
        self,
        update_data:TodoUpdate,
        todo_id:int,
        session:AsyncSession
    ):
        todo = await self.read_todo(todo_id,session)
        if todo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found"
            )
        update_data_dict = update_data.model_dump()
        for k,v in update_data_dict.items():
            setattr(todo,k,v)
        await session.commit()
        await session.refresh(todo)
        return todo    


    async def delete_todo(
        self,
        todo_id:int,
        session: AsyncSession
    ):
        todo = await self.read_todo(todo_id,session)

        if todo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found"
            )
        await session.delete(todo)
        await session.commit()    
        

