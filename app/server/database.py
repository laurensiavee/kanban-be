import motor.motor_asyncio
from bson.objectid import ObjectId

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

tasks_database = client.tasks

board_collection = tasks_database.get_collection("board_collection")
# task_collection = tasks_database.get_collection("task_collection")

# helpers
def board_helper(board) -> dict:
    print("board")
    print(board)
    return {
        "board_no": board["board_no"],
        "board_name": board["board_name"],
        "task_list": board["task_list"],
    }

##### board CRUD
# Retrieve all boards present in the database
async def retrieve_boards():
    boards = []
    async for board in board_collection.find():
        boards.append(board_helper(board))
    return boards

# Add a new board into to the database
async def add_board(board_data: dict) -> dict:
    board = await board_collection.insert_one(board_data)
    new_board = await board_collection.find_one({"_id": board.inserted_id})
    return board_helper(new_board)

