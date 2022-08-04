
from Server.Database import Workout_collection ,User_collection
from bson.objectid import ObjectId
import os
from ..Controller.User import User_helper
IMAGEDIR = os.getcwd()


def workout_helper(data) -> dict:
    return {
        "_id": str(data["_id"]),
        "TITLE": data["TITLE"],
        "DESCRIPTION": data["DESCRIPTION"],
        "GOAL": data["GOAL"],
        "LEVEL": data["LEVEL"],
        "BODYPART": data["BODYPART"],
        "EQUIPMENT": data["EQUIPMENT"],
        "DURATION": data["DURATION"],
        "PRICE": data["PRICE"],
        "DAY_1": data["DAY_1"],
        "DAY_2": data["DAY_2"],
        "DAY_3": data["DAY_3"],
        "DAY_4": data["DAY_4"],
        "DAY_5": data["DAY_5"],
        "DAY_6": data["DAY_6"],
        "DAY_7": data["DAY_7"],
        "STATUS": data["STATUS"],
        "IMAGE": data["IMAGE"],
    }


async def check_title(data):
    Titles = await Workout_collection.find_one({"TITLE": data})
    try:
        if Titles:
            return False
        else:
            return True
    except:
        return True


async def Delete_Old_Image(id: str):
    image = await Workout_collection.find_one({"_id": ObjectId(id)})
    try:
        Del_Img = str(image["IMAGE"]).split("%2F")
        Path = (
            str(IMAGEDIR)
            + chr(92)
            + "Server"
            + chr(92)
            + "Static"
            + chr(92)
            + str(Del_Img[-1]).replace("/", chr(92))
        )
        os.remove(Path)
    except:
        return "Error Ocured"
    return Path


async def Add_Workout(schema: dict) -> dict:
    Titles = await Workout_collection.insert_one(schema)
    return "Workout Successfully added"


async def retrieve_all_workouts():
    workout = []
    async for data in Workout_collection.find():
        workout.append(workout_helper(data))
    return workout


async def retrieve_workout_by_id(workout_id: str) -> dict:
    workout = await Workout_collection.find_one({"_id": ObjectId(workout_id)})
    if workout:
        return workout_helper(workout)
    else:
        return "Workout not found"

async def add_data(id:str, data):
    await User_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": {"Workout" : data}}
        )

async def delete_workout_data(id: str):
    data = await Workout_collection.find_one({"_id": ObjectId(id)})
    if data:
        
        async for user in User_collection.find():
                user_id=  str(user["_id"])
                user_workout= user["Workout"]
        
                if id in user_workout:
                     user_workout.remove(id)
                     await add_data(user_id,user_workout)
        
        await Workout_collection.delete_one({"_id": ObjectId(id)})
        return "Data Successfully deleted"
    return "Data Not Found"


async def update_workout(id: str, data: dict):
    if len(data) < 1:
        return False
    workout = await Workout_collection.find_one({"_id": ObjectId(id)})
    # if flags == 0:
    #     data["IMAGE"]=workout['IMAGE']
    if workout:
        updated_workout = await Workout_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_workout:
            return True
        return False
