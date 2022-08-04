from Server.Database import Recipes_collection , User_collection
from bson.objectid import ObjectId
import os

IMAGEDIR = os.getcwd()


def Recipes_helper(data) -> dict:
    return {
        "_id": str(data["_id"]),
        "TITLE": str(data["TITLE"]),
        "CATEGORY": data["CATEGORY"],
        "PRICE": data["PRICE"],
        "SERVINGS": data["SERVINGS"],
        "TOTAL_TIME": data["TOTAL_TIME"],
        "FEATURED": data["FEATURED"],
        "STATUS": data["STATUS"],
        "IMAGE": data["IMAGE"],
    }


def Single_Recipes_helper(data) -> dict:
    return {
        "_id": str(data["_id"]),
        "TITLE": str(data["TITLE"]),
        "DESCRIPTION": data["DESCRIPTION"],
        "INGREDIENTS": data["INGREDIENTS"],
        "DIRECTIONS": data["DIRECTIONS"],
        "CATEGORY": data["CATEGORY"],
        "PRICE": data["PRICE"],
        "CALORIES": data["CALORIES"],
        "CARBS": data["CARBS"],
        "PROTEIN": data["PROTEIN"],
        "FAT": data["FAT"],
        "SERVINGS": data["SERVINGS"],
        "TOTAL_TIME": data["TOTAL_TIME"],
        "FEATURED": data["FEATURED"],
        "STATUS": data["STATUS"],
        "IMAGE": data["IMAGE"],
    }


async def Check_Recipe(schema: dict):
    try:
        title = await Recipes_collection.find_one({"TITLE": schema["TITLE"]})
        if title:
            return False
        else:
            return True
    except:
        return True


async def Delete_Old_Image(id: str):
    image = await Recipes_collection.find_one({"_id": ObjectId(id)})
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


async def Add_Recipe(schema: dict) -> dict:

    await Recipes_collection.insert_one(schema)
    return "Recipes Successfully added"


async def retrieve_all_Recipess():
    recipes = []
    async for data in Recipes_collection.find():
        recipes.append(Recipes_helper(data))
    return recipes


async def retrieve_Recipes_by_id(recipes_id: str) -> dict:
    recipes = await Recipes_collection.find_one({"_id": ObjectId(recipes_id)})
    if recipes:
        return Single_Recipes_helper(recipes)
    else:
        return "No Recipes found by this id"

async def add_data(id:str, data):
    await User_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": {"Favourites_Recipes" : data}}
        )

async def delete_Recipes_data(id: str):
    data = await Recipes_collection.find_one({"_id": ObjectId(id)})
    if data:
        # Img_delte = await Delete_Old_Image(id)
        for user in User_collection.find():
            user_id = str(user["_id"])
            recipes_data= user['Favourites_Recipes']

            if id in recipes_data:
                recipes_data.remove(id)
                await add_data(user_id, recipes_data)
        await Recipes_collection.delete_one({"_id": ObjectId(id)})
        return "Data Successfully deleted"
    return "Data Not Found"


async def update_Recipes(id: str, data: dict, flags: int):
    if len(data) < 1:
        return False
    recipes = await Recipes_collection.find_one({"_id": ObjectId(id)})
    if flags == 0:
        data["IMAGE"] = recipes["IMAGE"]
    if recipes:
        updated_recipes = await Recipes_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_recipes:
            return True
        return False
