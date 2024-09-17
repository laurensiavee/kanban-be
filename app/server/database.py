import motor.motor_asyncio
from bson.objectid import ObjectId

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

tasks_database = client.tasks

board_collection = tasks_database.get_collection("board_collection")
# task_collection = tasks_database.get_collection("task_collection")

# helpers
def board_helper(board) -> dict:
    return {
        "board_no": board["board_no"],
        "board_name": board["board_name"],
        "task_list": board["task_list"],
    }

# Board
async def get_list_board():
    boards = []
    async for board in board_collection.find():
        boards.append(board_helper(board))
    return boards

async def get_board(board_no: str) -> dict:
    board = await board_collection.find_one({"board_no": board_no})
    if board:
        return board_helper(board)

async def add_board(board_data: dict) -> dict:
    board = await board_collection.insert_one(board_data)
    new_board = await board_collection.find_one({"_id": board.inserted_id})
    return board_helper(new_board)

async def update_board(board_no: str, data: dict):
    if len(data) < 1:
        return False
    board = await board_collection.find_one({"board_no": board_no})
    if board:
        updated_board = await board_collection.update_one(
            {"board_no": board_no}, {"$set": data}
        )
        if updated_board:
            return True
        return False

async def delete_board(board_no: str):
    board = await board_collection.find_one({"board_no": board_no})
    if board:
        await board_collection.delete_one({"board_no": board_no})
        return True



