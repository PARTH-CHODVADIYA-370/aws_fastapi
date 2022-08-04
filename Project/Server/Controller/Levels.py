from Server.Database import Levels_collection
from bson.objectid import ObjectId
import os

IMAGEDIR = os.getcwd()


def Levels_helper(data) -> dict:
    return {
        "_id": str(data["_id"]),
        "TITLE": data["TITLE"],
        "RATE": data["RATE"],
        "IMAGE": data["IMAGE"],
    }


async def Check_Level(schema: dict):
    try:
        title = await Levels_collection.find_one({"TITLE": schema["TITLE"]})
        if title:
            return False
        else:
            return True
    except:
        return True


async def Delete_Old_Image(id: str):
    image = await Levels_collection.find_one({"_id": ObjectId(id)})
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


async def Add_Level(schema: dict) -> dict:

    await Levels_collection.insert_one(schema)
    return "Level Successfully added"


async def retrieve_all_Levels():
    levels = []
    async for data in Levels_collection.find():
        levels.append(Levels_helper(data))
    return levels


async def retrieve_Level_by_id(level_id: str) -> dict:
    levels = await Levels_collection.find_one({"_id": ObjectId(level_id)})
    if levels:
        return Levels_helper(levels)


async def delete_Level_data(id: str):
    data = await Levels_collection.find_one({"_id": ObjectId(id)})
    if data:
        # Img_delete = await Delete_Old_Image(id)
        await Levels_collection.delete_one({"_id": ObjectId(id)})
        return "Data Successfully deleted"
    return "Data Not Found"


async def update_Level(id: str, data: dict, flags: int):
    if len(data) < 1:
        return False
    Level = await Levels_collection.find_one({"_id": ObjectId(id)})
    if flags == 0:
        data["IMAGE"] = Level["IMAGE"]
    if Level:
        updated_Level = await Levels_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_Level:
            return True
        return False
