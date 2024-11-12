import motor.motor_asyncio
from bson.objectid import ObjectId

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

kanban_database = client.kanban

board_collection = kanban_database.get_collection("board_collection")

# helpers
def board_helper(board) -> dict:
    return {
        "board_no": board["board_no"],
        "board_name": board["board_name"],
        "task_list": board["task_list"],
    }

# board
async def get_list_board():
    boards = []
    async for board in board_collection.find():
        boards.append(board_helper(board))
    return boards

async def get_board(board_no: str) -> dict:
    board = await board_collection.find_one({"board_no": board_no})
    if board:
        return board_helper(board)

async def add_board(data: dict) -> dict:
    board = await board_collection.insert_one(data)
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

# task
async def add_task(board_no: str, data: dict):
    board = await board_collection.find_one({"board_no": board_no})

    if board:
        updated_board = await board_collection.update_one(
            {"board_no": board_no},
            {"$push": {"task_list": data.dict()}}
        )

        if updated_board:
            return True
        return False

async def update_task(board_no: str, task_no: str, data: dict):
    if len(data) < 1:
        return False
    board = await board_collection.find_one({"board_no": board_no}, {"task_list.task_no": task_no})
    if board:
        updated_board = await board_collection.update_one(
            {"board_no": board_no, "task_list.task_no": task_no},
            {"$set": {'task_list.$[x]': data}},
            array_filters= [  {"x.task_no": task_no } ]
        )
        if updated_board:
            return True
        return False

async def update_task_state(board_no: str, task_no: str, state: str):
    if len(state) < 1:
        return False
    board = await board_collection.find_one({"board_no": board_no}, {"task_list.task_no": task_no})
    if board:
        updated_board = await board_collection.update_one(
            {"board_no": board_no, "task_list.task_no": task_no},
            {"$set": {'task_list.$[x].task_state': state}},
            array_filters= [  {"x.task_no": task_no } ]
        )
        if updated_board:
            return True
        return False

async def delete_task(board_no: str, task_no: str):
    board = await board_collection.find_one({"board_no": board_no}, {"task_list.task_no": task_no})
    if board:
        await board_collection.update_one(
            {"board_no": board_no, "task_list.task_no": task_no},
            {"$pull": {'task_list': {"task_no": task_no}}}
        )
        return True

# generate no

async def get_new_board_no() -> str:
    last_board = await board_collection.find_one()
    if last_board:
        return(generate_new_board_no(last_board["board_no"]))
    return "BOARD001"

async def get_new_task_no(board_no: str) -> str:
    board = await board_collection.find_one({"board_no": board_no})
    if board and board.get("task_list") and board["task_list"]:
        if board["task_list"][-1].get("task_no"):
            return generate_new_task_no(board["task_list"][-1]["task_no"])
    return "TASK001"

def generate_new_board_no(latest_board_no):
    num = latest_board_no[5:8]
    num = int(num) + 1
    str_num = str(num)
    pad = "000"
    new_task_no = "BOARD" + pad[:-len(str_num)] + str_num
    return new_task_no

def generate_new_task_no(latest_task_no):
    num = latest_task_no[4:7]
    num = int(num) + 1
    str_num = str(num)
    pad = "000"
    new_task_no = "TASK" + pad[:-len(str_num)] + str_num
    return new_task_no