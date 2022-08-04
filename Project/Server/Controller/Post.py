from Server.Database import Post_collection
from bson.objectid import ObjectId
import os

IMAGEDIR = os.getcwd()


def Post_helper(data) -> dict:
    return {
        "_id": str(data["_id"]),
        "TITLE": data["TITLE"],
        "TAG": data["TAG"],
        "FEATURED": data["FEATURED"],
        "STATUS": data["STATUS"],
        "IMAGE": data["IMAGE"],
    }


def Single_Post_helper(data) -> dict:
    return {
        "_id": str(data["_id"]),
        "TITLE": data["TITLE"],
        "DESCRIPTION": data["DESCRIPTION"],
        "TAG": data["TAG"],
        "FEATURED": data["FEATURED"],
        "STATUS": data["STATUS"],
        "IMAGE": data["IMAGE"],
    }


async def Check_Post(schema: dict):
    try:
        title = await Post_collection.find_one({"TITLE": schema["TITLE"]})
        if title:
            return False
        else:
            return True
    except:
        return True


async def Delete_Old_Image(id: str):
    image = await Post_collection.find_one({"_id": ObjectId(id)})
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


async def Add_Post(schema: dict) -> dict:
    await Post_collection.insert_one(schema)
    return "Post Successfully added"


async def retrieve_all_Post():
    post = []
    async for data in Post_collection.find():
        post.append(Post_helper(data))
    return post


async def retrieve_Post_by_id(post_id: str) -> dict:
    post = await Post_collection.find_one({"_id": ObjectId(post_id)})
    if post:
        return Single_Post_helper(post)


async def delete_Post_data(id: str):
    data = await Post_collection.find_one({"_id": ObjectId(id)})
    if data:
        # Img_delete = await Delete_Old_Image(id)
        await Post_collection.delete_one({"_id": ObjectId(id)})
        return "Data Successfully deleted"
    return "Data Not Found"


async def update_Post(id: str, data: dict, flags: int):
    if len(data) < 1:
        return False
    post = await Post_collection.find_one({"_id": ObjectId(id)})
    if flags == 0:
        data["IMAGE"] = post["IMAGE"]
    if post:
        updated_post = await Post_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_post:
            return True
        return False
