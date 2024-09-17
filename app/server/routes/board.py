from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from ..database import (
    get_list_board,
    get_board,
    add_board,
    update_board,
    delete_board
)

from ..models.board import (
    ErrorResponseModel,
    ResponseModel,
    BoardSchema,
)

router = APIRouter()

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

@router.put("/{board_no}")
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
            "Board with ID: {} removed".format(board_no), "Board deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Board with id {0} doesn't exist".format(board_no)
    )

