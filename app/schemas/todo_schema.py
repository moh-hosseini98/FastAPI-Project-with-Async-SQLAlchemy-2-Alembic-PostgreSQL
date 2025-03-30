from datetime import datetime
from pydantic import BaseModel

class TodoBase(BaseModel):
    content : str 
    

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    pass

class TodoRead(TodoBase):
    id : int
    created_at : datetime
    updated_at : datetime


