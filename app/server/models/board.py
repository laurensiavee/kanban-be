from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from .task import TaskSchema as Task

class BoardSchema(BaseModel):
    board_no: str = Field(...)
    board_name: str = Field(...)
    task_list: list[Task] | None = None

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code"  : code, "message": message}