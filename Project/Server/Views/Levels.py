import base64
import uuid
from fastapi import APIRouter, Body
from Server.Utils.Image_Handler import Image_Converter
from Server.Controller.Levels import (
    Add_Level,
    Delete_Old_Image,
    Check_Level,
    delete_Level_data,
    retrieve_all_Levels,
    retrieve_Level_by_id,
    update_Level,
)
from Server.Models.Levels import Levels
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.post("/", response_description="Add Level")
async def add_Levels_data(schema: Levels = Body(...)):
    schema = jsonable_encoder(schema)
    levels = await Check_Level(schema)
    if levels == False:
        return {"code": 409, "Msg": "Levels already exists"}
    if len(schema["IMAGE"]) > 0:
        img_path = await Image_Converter(schema["IMAGE"])
    else:
        img_path = ""
    schema["IMAGE"] = str(img_path)
    output = await Add_Level(schema)
    return {"code": 200, "Msg": output}


@router.get("/", response_description="Get all Levels")
async def get_all_Levels():
    levels = await retrieve_all_Levels()
    if levels:
        return {"code": 200, "Data": levels}
    return {"Data": levels, "Msg": "Empty list return"}


@router.get("/{id}", response_description="Get Level data by id")
async def get_Level_data(id):
    data = await retrieve_Level_by_id(id)
    if data:
        return {"code": 200, "Data": data}
    return {"Msg": "Id may not exist"}


@router.delete("/{id}", response_description="Delete Level data by id")
async def delete_Level(id: str):
    data = await delete_Level_data(id)
    if data:
        return {"code": 200, "Msg": data}
    return {"Msg": "Id may not exist"}


@router.put("/{id}")
async def update_Level_data(id: str, req: Levels = Body(...)):
    req = jsonable_encoder(req)
    req = {q: s for q,s in req.items() if len(str(s))!=0}
    flags = 0
    if len(req["IMAGE"]) != 0:
        # Del_img= await Delete_Old_Image(id)
        img_path = await Image_Converter(req["IMAGE"])
        req["IMAGE"] = img_path
        flags = 1
    updated_level = await update_Level(id, req, flags)
    if updated_level:
        return {"code": 200, "Data": "Data updated Successfully"}

    return {"code": 404, "Data": "Something Went Wrong"}
