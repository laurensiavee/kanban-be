from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class TaskSchema(BaseModel):
    task_no: str = Field(...)
    task_state: str = Field(...)
    task_title: str = Field(...)
    task_desc: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "task_no": "Task001",
                "task_state": "todo",
                "task_title": "Refactor add task",
                "task_desc": "Refactor add task method to be readable and work porperly.",
            }
        }

