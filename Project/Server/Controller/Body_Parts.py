from audioop import add
import re
from tkinter import E
from Server.Database import Bodyparts_collection ,Exercise_collection ,Workout_collection
from bson.objectid import ObjectId
import os

IMAGEDIR = os.getcwd()


def bodyparts_helper(data) -> dict:
    return {
        "_id": str(data["_id"]),
        "TITLE": data["TITLE"],
        "IMAGE": data["IMAGE"],
    }


async def check_bodypart(schema: dict):
    try:
        title = await Bodyparts_collection.find_one({"TITLE": schema["TITLE"]})
        if title:
            return False
        else:
            return True
    except Exception as e:
        return e


async def delete_old_image(id: str):
    image = await Bodyparts_collection.find_one({"_id": ObjectId(id)})
    try:
        del_img = str(image["IMAGE"]).split("%2F")
        path = (
            str(IMAGEDIR)
            + chr(92)
            + "Server"
            + chr(92)
            + "Static"
            + chr(92)
            + str(del_img[-1]).replace("/", chr(92))
        )
        os.remove(path)
    except:
        return "Error Ocured"
    return path


async def add_bodypart(schema: dict):
    try:
        await Bodyparts_collection.insert_one(schema)
        return "Body Part Successfully added"
    except Exception as e:
        return e.args


async def retrieve_all_bodyparts():
    bodyparts = []
    async for data in Bodyparts_collection.find():
        bodyparts.append(bodyparts_helper(data))
    return bodyparts


async def retrieve_bodypart_by_id(bodypart_id: str) -> dict:
    try:
        bodyparts = await Bodyparts_collection.find_one({"_id": ObjectId(bodypart_id)})
        if bodyparts:
            return bodyparts_helper(bodyparts)
    except Exception as e:
        return e.args

async def add_data(id:str, data):
    await Exercise_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": {"Bodypart" : data}}
        )

async def update_workout(id: str, data: dict):
    await Workout_collection.update_one({"_id": ObjectId(id)}, {"EQUIPMENT" : data})

async def delete_bodypart_data(id: str):
    data = await Bodyparts_collection.find_one({"_id": ObjectId(id)})
    if data:
        # Img_delete = await Delete_Old_Image(id)
        for exercise in Exercise_collection.find():
            exercise_id =str(exercise['_id'])
            exercise_bodypart = exercise['Bodypart'] 

            if id in exercise_bodypart:
                exercise_bodypart.remove(id)
                await add_data(exercise_id, exercise_bodypart)
        for workout in Workout_collection.find():
            workout_id= str(workout['_id'])
            workout_data= workout['EQUIPMENT']
            if id in workout_data:
                workout_data.remove(id)
                await add_data(workout_id, workout_data)
        await Bodyparts_collection.delete_one({"_id": ObjectId(id)})
        return "Data Successfully deleted"
    return "Data Not Found"


async def update_bodypart(id: str, data: dict, flags: int):
    if len(data) < 1:
        return False
    bodypart = await Bodyparts_collection.find_one({"_id": ObjectId(id)})
    if flags == 0:
        data["IMAGE"] = bodypart["IMAGE"]
    if bodypart:
        updated_bodypart = await Bodyparts_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_bodypart:
            return True
        return False
