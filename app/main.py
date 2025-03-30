from fastapi import FastAPI
from api.todos import router
from core.db import init_db


app = FastAPI(
    title='todoAPI',
    description='A RESTful API for a todo web service',
    version='v1',
)

@app.on_event("startup")
async def on_startup():
    await init_db()




app.include_router(router,prefix="/api/v1/todos",tags=["todos"])