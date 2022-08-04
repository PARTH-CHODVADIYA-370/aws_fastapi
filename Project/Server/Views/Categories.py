from fastapi import APIRouter, Body
from Server.Utils.Image_Handler import Image_Converter
from Server.Controller.Categories import (
    check_categories,
    add_category,
    retrieve_all_categories,
    retrieve_category_by_id,
    update_category,
    delete_category_data,
)
from Server.Models.Categories import Categories
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.post("/", response_description="Add Category")
async def add_categories_data(schema: Categories = Body(...)):
    schema = jsonable_encoder(schema)
    category = await check_categories(schema)
    if category == False:
        return {"code": 409, "Msg": "Categories already exists"}
    if len(schema["IMAGE"]) > 0:
        img_path = await Image_Converter(schema["IMAGE"])
    else:
        img_path = ""
    schema["IMAGE"] = str(img_path)
    output = await add_category(schema)
    return {"code": 200, "Msg": output}


@router.get("/", response_description="Get all Categories")
async def get_all_categories():
    categories = await retrieve_all_categories()
    if categories:
        return {"code": 200, "Data": categories}
    return {"Data": categories, "Msg": "Empty list return"}


@router.get("/{id}", response_description="Get Category data by id")
async def get_category_data(id):
    data = await retrieve_category_by_id(id)
    if data:
        return {"code": 200, "Data": data}
    return {"Msg": "Id may not exist"}


@router.delete("/{id}", response_description="Delete Category data by id")
async def delete_category(id: str):
    data = await delete_category_data(id)
    if data:
        return {"code": 200, "Msg": data}
    return {"Msg": "Id may not exist"}


@router.put("/{id}")
async def update_category_data(id: str, req: Categories = Body(...)):
    req = jsonable_encoder(req)
    req = {q: s for q,s in req.items() if len(str(s))!=0}
    flags = 0
    if len(req["IMAGE"]) != 0:
        # Del_img= await Delete_Old_Image(id)
        image_path = await Image_Converter(req["IMAGE"])
        req["IMAGE"] = image_path
        flags = 1
    updated_category = await update_category(id, req, flags)
    if updated_category:
        return {"code": 200, "Data": "Data updated Successfully"}

    return {"code": 404, "Data": "Something Went Wrong"}
