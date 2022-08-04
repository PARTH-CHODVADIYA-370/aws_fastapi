
from fastapi import APIRouter, Body
from Server.Utils.Image_Handler import Image_Converter
from Server.Controller.Equipments import (
    check_eqipment,
    add_equipment,
    retrieve_all_equipments,
    retrieve_equipment_by_id,
    delete_equipment_data,
    update_equipment,
)
from Server.Models.Equipments import Equipments
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.post("/", response_description="Add Equipment")
async def add_equipments_data(schema: Equipments = Body(...)):
    schema = jsonable_encoder(schema)
    equipment = await check_eqipment(schema)
    if equipment == False:
        return {"code": 409, "Msg": "Equipments already exists"}
    if len(schema["IMAGE"]) > 0:
        img_path = await Image_Converter(schema["IMAGE"])
    else:
        img_path = ""
    schema["IMAGE"] = str(img_path)
    output = await add_equipment(schema)
    return {"code": 200, "Msg": output}


@router.get("/", response_description="Get all Equipments")
async def get_all_equipments():
    equipments = await retrieve_all_equipments()
    if equipments:
        return {"code": 200, "Data": equipments}
    return {"Data": equipments, "Msg": "Empty list return"}


@router.get("/{id}", response_description="Get Equipment data by id")
async def get_equipment_data(id):
    data = await retrieve_equipment_by_id(id)
    if data:
        return {"code": 200, "Data": data}
    return {"Msg": "Id may not exist"}


@router.delete("/{id}", response_description="Delete Equipment data by id")
async def delete_equipment(id: str):
    data = await delete_equipment_data(id)
    if data:
        return {"code": 200, "Msg": data}
    return {"Msg": "Id may not exist"}


@router.put("/{id}")
async def update_equipment_data(id: str, req: Equipments = Body(...)):
    req = jsonable_encoder(req)
    req = {q: s for q,s in req.items() if len(str(s))!=0}
    flags = 0
    if len(req["IMAGE"]) != 0:
        # Del_img= await Delete_Old_Image(id)
        image_path = await Image_Converter(req["IMAGE"])
        req["IMAGE"] = image_path
        flags = 1
    updated_equipment = await update_equipment(id, req, flags)
    if updated_equipment:
        return {"code": 200, "Data": "Data updated Successfully"}

    return {"code": 404, "Data": "Something Went Wrong"}
