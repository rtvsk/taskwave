import os
import sys

sys.path.append(os.getcwd())

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.auth.routers import auth_router
from src.tasks.routers import tasks_router
from src.tasks_group.routers import tasks_group_router
from src.users.routers import users_router

app = FastAPI(title="Reminder")

# Define origins that you want to allow
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# Add middleware to handle CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
)

routers = (
    auth_router,
    tasks_router,
    tasks_group_router,
    users_router,
)
for router in routers:
    app.include_router(router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
