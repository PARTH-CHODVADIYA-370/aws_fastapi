from fastapi import APIRouter, Body
from Server.Database import Recipes_collection
from Server.Utils.Image_Handler import Image_Converter
from Server.Controller.Recipe import (
    Add_Recipe,
    Delete_Old_Image,
    Check_Recipe,
    delete_Recipes_data,
    retrieve_all_Recipess,
    retrieve_Recipes_by_id,
    update_Recipes,
)
from Server.Models.Recipe import Recipe
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.post("/", response_description="Add Recipe")
async def add_recipe_data(schema: Recipe = Body(...)):
    schema = jsonable_encoder(schema)
    recipes = await Check_Recipe(schema)
    if recipes == False:
        return {"code": 404, "Msg": "Recipe already exists"}
    if len(schema["IMAGE"]) > 0:
        img_path = await Image_Converter(schema["IMAGE"])
    else:
        img_path = ""
    schema["IMAGE"] = str(img_path)
    output = await Add_Recipe(schema)
    return {"code": 200, "Msg": output}


@router.get("/", response_description="Get all Recipe")
async def get_all_Recipe():
    recipe = await retrieve_all_Recipess()
    if recipe:
        return {"code": 200, "Data": recipe}
    return {"Data": recipe, "Msg": "Empty list return"}


@router.get("/{id}", response_description="Get Recipe data by id")
async def get_recipe_data(id):
    data = await retrieve_Recipes_by_id(id)
    if data:
        return {"code": 200, "Data": data}
    return {"Msg": "Id may not exist"}


@router.delete("/{id}", response_description="Delete Recipe data by id")
async def delete_recipe(id: str):
    data = await delete_Recipes_data(id)
    if data:
        return {"code": 200, "Msg": data}
    return {"Msg": "Id may not exist"}


@router.put("/{id}")
async def update_Recipe_data(id: str, req: Recipe = Body(...)):
    req = jsonable_encoder(req)
    req = {q: s for q,s in req.items() if len(str(s))!=0}
    flags = 0
    if len(req["IMAGE"]) != 0:
        # Del_img= await Delete_Old_Image(id)
        img_path = await Image_Converter(req["IMAGE"])
        req["IMAGE"] = img_path
        flags = 1
    updated_recipe = await update_Recipes(id, req, flags)
    if updated_recipe:
        return {"code": 200, "Data": "Data updated Successfully"}

    return {"code": 404, "Data": "Something Went Wrong"}


@router.post("/{id}", response_description="Change Status of Recipe")
async def Change_Recipe_Status(id: str):
    data = await Recipes_collection.find_one({"_id": ObjectId(id)})
    if data:
        if data["STATUS"] == "ACTIVE":
            await Recipes_collection.update_one(
                {"_id": ObjectId(id)}, {"$set": {"STATUS": "Inactive"}}
            )
        else:
            await Recipes_collection.update_one(
                {"_id": ObjectId(id)}, {"$set": {"STATUS": "ACTIVE"}}
            )
        return {"code": 404, "Data": "Something Went Wrong"}
    return {"code": 404, "Data": "Id may not exist"}
