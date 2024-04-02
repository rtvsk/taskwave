from src.exceptions import NotFoundException


class TaskNotFound(NotFoundException):
    def __init__(self, detail: str = "Task not found"):
        super().__init__(detail=detail)
