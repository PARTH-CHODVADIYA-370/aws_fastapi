from sys import flags
from fastapi import APIRouter, Body
from Server.Utils.Image_Handler import Image_Converter
from Server.Controller.Subscription import (
    Delete_Old_Image,
    Check_Subscriptions,
    Add_Subscriptions,
    retrieve_all_Subscriptions,
    retrieve_Subscriptions_by_id,
    delete_Subscriptions_data,
    update_Subscriptions,
)
from Server.Database import Subscription_collection
from Server.Models.Subscription import Subscriptions
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.post("/", response_description="Add Subscriptions")
async def add_Subscription_data(schema: Subscriptions = Body(...)):
    schema = jsonable_encoder(schema)
    subscriptions = await Check_Subscriptions(schema)
    if subscriptions == False:
        return {"code": 404, "Msg": "Subscription already exists"}

    if len(schema["IMAGE"]) > 0:
        img_path = await Image_Converter(schema["IMAGE"])
    else:
        img_path = ""
    schema["IMAGE"] = str(img_path)
    output = await Add_Subscriptions(schema)
    return {"code": 200, "Msg": output}


@router.get("/", response_description="Get all Subscriptions")
async def get_all_Subscriptions():
    subscriptions = await retrieve_all_Subscriptions()
    if subscriptions:
        return {"code": 200, "Data": subscriptions}
    return {"Data": subscriptions, "Msg": "Empty list return"}


@router.get("/{id}", response_description="Get Subscriptions data by id")
async def get_Subscriptions_data(id):
    data = await retrieve_Subscriptions_by_id(id)
    if data:
        return {"code": 200, "Data": data}
    return {"Msg": "Id may not exist"}


@router.delete("/{id}", response_description="Delete Subscriptions data by id")
async def delete_Subscriptions(id: str):
    data = await delete_Subscriptions_data(id)
    if data:
        return {"code": 200, "Msg": data}
    return {"Msg": "Id may not exist"}


@router.put("/{id}")
async def update_Subscriptions_data(id: str, req: Subscriptions = Body(...)):
    req = jsonable_encoder(req)
    req = {q: s for q,s in req.items() if len(str(s))!=0}
    flags = 0
    if len(req["IMAGE"]) != 0:
        # del_img = await Delete_Old_Image(id)
        img_path = await Image_Converter(req["IMAGE"])
        req["IMAGE"] = img_path
        flags = 1
    updated_subscriptions = await update_Subscriptions(id, req, flags)
    if updated_subscriptions:
        return {"code": 200, "Data": "Data updated Successfully"}
    return {"code": 200, "Msg": "Id may not exist"}


@router.post("/{id}", response_description="Change Subscriptions status")
async def change_Subscriptions_status(id: str):
    data = await Subscription_collection.find_one({"_id": ObjectId(id)})
    if data:
        if data["STATUS"] == "ACTIVE":
            await Subscription_collection.update_one(
                {"_id": ObjectId(id)}, {"$set": {"STATUS": "INACTIVE"}}
            )
        else:
            await Subscription_collection.update_one(
                {"_id": ObjectId(id)}, {"$set": {"STATUS": "ACTIVE"}}
            )
        return {"code": 200, "Msg": "Status changed Successfully"}
    return {"code": 200, "Msg": "Id may not exist"}
