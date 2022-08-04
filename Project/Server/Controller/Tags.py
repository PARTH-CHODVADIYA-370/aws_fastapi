from Server.Database import Tags_collection
from bson.objectid import ObjectId


def Tags_helper(data) -> dict:
    return {
        "_id": str(data["_id"]),
        "TITLE": data["TITLE"],
    }


async def Add_Tag(schema: dict) -> dict:

    try:
        title = await Tags_collection.find_one({"TITLE": schema["TITLE"]})
        if title:
            return "Tag is  already in the collection"
        else:
            title = await Tags_collection.insert_one(schema)
            return "Tag Successfully added"
    except:
        title = await Tags_collection.insert_one(schema)
        return "Tag Successfully added"


async def retrieve_all_Tags():
    tags = []
    async for data in Tags_collection.find():
        tags.append(Tags_helper(data))
    return tags


async def retrieve_Tag_by_id(tag_id: str) -> dict:
    tags = await Tags_collection.find_one({"_id": ObjectId(tag_id)})
    if tags:
        return Tags_helper(tags)


async def delete_Tag_data(id: str):
    data = await Tags_collection.find_one({"_id": ObjectId(id)})
    if data:
        await Tags_collection.delete_one({"_id": ObjectId(id)})
        return "Data Successfully deleted"
    return "Data Not Found"


async def update_Tag(id: str, data: dict):
    if len(data) < 1:
        return False
    tags = await Tags_collection.find_one({"_id": ObjectId(id)})
    if tags:
        updated_tag = await Tags_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_tag:
            return True
        return False
