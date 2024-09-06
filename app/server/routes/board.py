from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from ..database import (
    retrieve_boards,
    add_board,
)

from ..models.board import (
    ErrorResponseModel,
    ResponseModel,
    BoardSchema,
)

router = APIRouter()

@router.get("/", response_description="Boards retrieved")
async def get_boards():
    boards = await retrieve_boards()
    if boards:
        return ResponseModel(boards, "Boards data retrieved successfully")
    return ResponseModel(boards, "Empty list returned")

@router.post("/", response_description="Board data added into the database")
async def add_board_data(board: BoardSchema = Body(...)):
    board = jsonable_encoder(board)
    new_board = await add_board(board)
    return ResponseModel(new_board, "Board added successfully.")