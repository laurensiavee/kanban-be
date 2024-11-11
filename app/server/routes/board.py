from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from ..database import (
    get_list_board,
    get_board,
    add_board,
    update_board,
    delete_board,
    add_task,
    update_task,
    update_task_state,
    delete_task,
    get_latest_board_no,
    get_latest_task_no,
)

from ..models.board import (
    ErrorResponseModel,
    ResponseModel,
    BoardSchema,
)

from ..models.task import (
    TaskSchema,
)

router = APIRouter()

# board
@router.get("/list", response_description="Boards retrieved")
async def get_list_board_data():
    boards = await get_list_board()
    if boards:
        return ResponseModel(boards, "Boards data retrieved successfully")
    return ResponseModel(boards, "Empty list returned")

@router.get("/{board_no}", response_description="Board data retrieved")
async def get_board_data(board_no):
    board = await get_board(board_no)
    if board:
        return ResponseModel(board, "Board data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Board doesn't exist.")

@router.post("/", response_description="Board data added into the database")
async def add_board_data(board: BoardSchema = Body(...)):
    board = jsonable_encoder(board)
    new_board = await add_board(board)
    return ResponseModel(new_board, "Board added successfully.")

@router.put("/{board_no}", response_description="Board data updated into the database")
async def update_board_data(board_no: str, req: BoardSchema = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_board = await update_board(board_no, req)
    if updated_board:
        return ResponseModel(
            "Board with ID: {} name update is successful".format(board_no),
            "Board name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the board data.",
    )

@router.delete("/{board_no}", response_description="Board data deleted from the database")
async def delete_board_data(board_no: str):
    deleted_board = await delete_board(board_no)
    if deleted_board:
        return ResponseModel(
            "Board with ID: {} removed".format(board_no), 
            "Board deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Board with id {0} doesn't exist".format(board_no)
    )

# task
@router.post("/{board_no}/task/", response_description="Task data added into the database")
async def add_task_data(board_no: str, req: TaskSchema = Body(...)):
    new_task = await add_task(board_no, req)
    return ResponseModel(new_task, "Task added successfully.")

@router.put("/{board_no}/task/{task_no}", response_description="Task data updated into the database")
async def update_task_data(board_no: str, task_no: str, req: TaskSchema = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_task = await update_task(board_no, task_no, req)
    if updated_task:
        return ResponseModel(
            "Task with ID: {} name update is successful".format(task_no),
            "Task name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the task data.",
    )

@router.put("/{board_no}/task/{task_no}/state/{task_state}", response_description="Task data updated into the database")
async def update_task_state_data(board_no: str, task_no: str, task_state: str):
    updated_task = await update_task_state(board_no, task_no, task_state)
    if updated_task:
        return ResponseModel(
            "Task with ID: {} name update is successful".format(task_no),
            "Task name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the task data.",
    )

@router.delete("/{board_no}/task/{task_no}", response_description="Task data deleted into the database")
async def delete_task_data(board_no: str, task_no: str):
    updated_task = await delete_task(board_no, task_no)
    if updated_task:
        return ResponseModel(
            "Task with ID: {} name delete is successful".format(task_no),
            "Task name deleted successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the task data.",
    )
