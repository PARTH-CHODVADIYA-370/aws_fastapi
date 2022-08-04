from Server.Database import Goals_collection
from bson.objectid import ObjectId
import os

IMAGEDIR = os.getcwd()


def Goals_helper(data) -> dict:
    return {
        "_id": str(data["_id"]),
        "TITLE": data["TITLE"],
        "DESCRIPTION": data["DESCRIPTION"],
        "IMAGE": data["IMAGE"],
    }


async def Check_Goal(schema: dict):
    try:
        title = await Goals_collection.find_one({"TITLE": schema["TITLE"]})
        if title:
            return False
        else:
            return True
    except:
        return True


async def Delete_Old_Image(id: str):
    image = await Goals_collection.find_one({"_id": ObjectId(id)})
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


async def Add_Goal(schema: dict) -> dict:
    await Goals_collection.insert_one(schema)
    return "Goal Successfully added"


async def retrieve_all_Goals():
    goals = []
    async for data in Goals_collection.find():
        goals.append(Goals_helper(data))
    return goals


async def retrieve_Goal_by_id(goal_id: str) -> dict:
    goals = await Goals_collection.find_one({"_id": ObjectId(goal_id)})
    if goals:
        return Goals_helper(goals)


async def delete_Goal_data(id: str):
    data = await Goals_collection.find_one({"_id": ObjectId(id)})
    if data:
        
        # Img_delete = await Delete_Old_Image(id)
        await Goals_collection.delete_one({"_id": ObjectId(id)})
        return "Data Successfully deleted"
    return "Data Not Found"


async def update_Goal(id: str, data: dict, flags: int):
    if len(data) < 1:
        return False
    goal = await Goals_collection.find_one({"_id": ObjectId(id)})
    if flags == 0:
        data["IMAGE"] = goal["IMAGE"]
    if goal:
        updated_goal = await Goals_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_goal:
            return True
        return False
