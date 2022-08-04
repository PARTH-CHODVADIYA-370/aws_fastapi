from Server.Database import Categories_collection
from bson.objectid import ObjectId
import os

IMAGEDIR = os.getcwd()


def categories_helper(data) -> dict:
    return {
        "_id": str(data["_id"]),
        "TITLE": data["TITLE"],
        "IMAGE": data["IMAGE"],
    }


async def check_categories(schema: dict):
    try:
        title = await Categories_collection.find_one({"TITLE": schema["TITLE"]})
        if title:
            return False
        else:
            return True
    except Exception as e:
        return e.args


async def delete_old_image(id: str):
    image = await Categories_collection.find_one({"_id": ObjectId(id)})
    try:
        delimg = str(image["IMAGE"]).split("%2F")
        path = (
            str(IMAGEDIR)
            + chr(92)
            + "Server"
            + chr(92)
            + "Static"
            + chr(92)
            + str(delimg[-1]).replace("/", chr(92))
        )
        os.remove(path)
    except:
        return "Error Ocured"
    return path


async def add_category(schema: dict) -> dict:

    Title = await Categories_collection.insert_one(schema)
    return "Category Successfully added"


async def retrieve_all_categories():
    Categories = []
    async for data in Categories_collection.find():
        Categories.append(categories_helper(data))
    return Categories


async def retrieve_category_by_id(Category_id: str) -> dict:
    Categories = await Categories_collection.find_one({"_id": ObjectId(Category_id)})
    if Categories:
        return categories_helper(Categories)


async def delete_category_data(id: str):
    data = await Categories_collection.find_one({"_id": ObjectId(id)})
    if data:
        # Img_delete = await Delete_Old_Image(id)
        await Categories_collection.delete_one({"_id": ObjectId(id)})
        return "Data Successfully deleted"
    return "Data Not Found"


async def update_category(id: str, data: dict, flags: int):
    if len(data) < 1:
        return False
    category = await Categories_collection.find_one({"_id": ObjectId(id)})
    if flags == 0:
        data["IMAGE"] = category["IMAGE"]
    if category:
        updated_category = await Categories_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_category:
            return True
        return False
