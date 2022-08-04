
from Server.Database import Equipments_collection ,Exercise_collection,Workout_collection
from bson.objectid import ObjectId
import os

IMAGEDIR = os.getcwd()


def equipments_helper(data) -> dict:
    return {
        "_id": str(data["_id"]),
        "TITLE": data["TITLE"],
        "IMAGE": data["IMAGE"],
    }


async def check_eqipment(schema: dict):
    try:
        title = await Equipments_collection.find_one({"TITLE": schema["TITLE"]})
        if title:
            return False
        else:
            return True
    except:
        return True


async def dlete_old_image(id: str):
    image = await Equipments_collection.find_one({"_id": ObjectId(id)})
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


async def add_equipment(schema: dict) -> dict:
    await Equipments_collection.insert_one(schema)
    return "Equipment Successfully added"


async def retrieve_all_equipments():
    equipments = []
    async for data in Equipments_collection.find():
        equipments.append(equipments_helper(data))
    return equipments


async def retrieve_equipment_by_id(Equipment_id: str) -> dict:
    equipments = await Equipments_collection.find_one({"_id": ObjectId(Equipment_id)})
    if equipments:
        return equipments_helper(equipments)

async def add_data(id:str, data):
    await Exercise_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": {"EQUIPMENT" : data}}
        )

async def update_workout(id: str, data: dict):
    await Workout_collection.update_one({"_id": ObjectId(id)}, {"EQUIPMENT" : data})


async def delete_equipment_data(id: str):
    data = await Equipments_collection.find_one({"_id": ObjectId(id)})
    if data:
        # Img_delete = await Delete_Old_Image(id)
        for exercise in Exercise_collection.find():
            exercise_id= str(exercise['_id'])
            exercise_data= exercise['EQUIPMENT']
            if id in exercise_data:
                exercise_data.remove(id)
                await add_data(exercise_id, exercise_data)
        for workout in Workout_collection.find():
            workout_id= str(workout['_id'])
            workout_data= workout['EQUIPMENT']
            if id in workout_data:
                workout_data.remove(id)
                await update_workout(workout_id, workout_data)

        await Equipments_collection.delete_one({"_id": ObjectId(id)})
        return "Data Successfully deleted"
    return "Data Not Found"


async def update_equipment(id: str, data: dict, flags: int):
    if len(data) < 1:
        return False
    equipment = await Equipments_collection.find_one({"_id": ObjectId(id)})
    if flags == 0:
        data["IMAGE"] = equipment["IMAGE"]
    if equipment:
        updated_equipment = await Equipments_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_equipment:
            return True
        return False
