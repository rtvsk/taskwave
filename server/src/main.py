import os
import sys

sys.path.append(os.getcwd())

import uvicorn
from fastapi import FastAPI

from src.auth.routers import auth_router
from src.tasks.routers import tasks_router
from src.tasks_group.routers import tasks_group_router
from src.users.routers import users_router

app = FastAPI(title="Reminder")

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(tasks_group_router)
app.include_router(tasks_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
