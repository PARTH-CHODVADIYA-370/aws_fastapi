from Server.Database import Subscription_collection
from bson.objectid import ObjectId
import os

IMAGEDIR = os.getcwd()


def Subscriptions_helper(data) -> dict:
    return {
        "_id": str(data["_id"]),
        "NAME": str(data["NAME"]),
        "DURATION": data["DURATION"],
        "DESCRIPTION": data["DESCRIPTION"],
        "PRICE": data["PRICE"],
        "STATUS": data["STATUS"],
        "IMAGE": data["IMAGE"],
    }


async def Check_Subscriptions(schema: dict):
    try:
        NAME = await Subscription_collection.find_one({"NAME": schema["NAME"]})
        if NAME:
            return False
        else:
            return True
    except:
        return True


async def Delete_Old_Image(id: str):
    image = await Subscription_collection.find_one({"_id": ObjectId(id)})
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


async def Add_Subscriptions(schema: dict) -> dict:
    await Subscription_collection.insert_one(schema)
    return "Subscriptions Successfully added"


async def retrieve_all_Subscriptions():
    recipes = []
    async for data in Subscription_collection.find():
        recipes.append(Subscriptions_helper(data))
    return recipes


async def retrieve_Subscriptions_by_id(recipes_id: str) -> dict:
    recipes = await Subscription_collection.find_one({"_id": ObjectId(recipes_id)})
    if recipes:
        return Subscriptions_helper(recipes)
    else:
        return "No Recipes found by this id"


async def delete_Subscriptions_data(id: str):
    data = await Subscription_collection.find_one({"_id": ObjectId(id)})
    if data:
        # Img_delte = await Delete_Old_Image(id)
        await Subscription_collection.delete_one({"_id": ObjectId(id)})
        return "Data Successfully deleted"
    return "Data Not Found"


async def update_Subscriptions(id: str, data: dict, flags: int):
    if len(data) < 1:
        return False
    subscriptions = await Subscription_collection.find_one({"_id": ObjectId(id)})
    if flags == 0:
        data["IMAGE"] = subscriptions["IMAGE"]
    if subscriptions:
        updated_subscriptions = await Subscription_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_subscriptions:
            return True
        return False
