import motor.motor_asyncio
from bson.objectid import ObjectId

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

# tasks_database = client.tasks

# board_collection = tasks_database.get_collection("board_collection")
# task_collection = tasks_database.get_collection("task_collection")
