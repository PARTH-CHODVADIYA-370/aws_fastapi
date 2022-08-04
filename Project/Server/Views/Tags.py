from fastapi import APIRouter, Body
from Server.Controller.Tags import (
    Add_Tag,
    delete_Tag_data,
    retrieve_all_Tags,
    retrieve_Tag_by_id,
    update_Tag,
)
from Server.Models.Tags import Tags
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.post("/", response_description="Add Tag")
async def add_Tags_data(schema: Tags = Body(...)):
    schema = jsonable_encoder(schema)
    output = await Add_Tag(schema)
    return {"code": 200, "Msg": output}


@router.get("/", response_description="Get all Tags")
async def get_all_Tags():
    tags = await retrieve_all_Tags()
    if tags:
        return {"code": 200, "Data": tags}
    return {"Data": tags, "Msg": "Empty list return"}


@router.get("/{id}", response_description="Get Tag data by id")
async def get_Tag_data(id):
    data = await retrieve_Tag_by_id(id)
    if data:
        return {"code": 200, "Data": data}
    return {"Msg": "Id may not exist"}


@router.delete("/{id}", response_description="Delete Tag data by id")
async def delete_Tag(id: str):
    data = await delete_Tag_data(id)
    if data:
        return {"code": 200, "Msg": data}
    return {"code":404,"Msg": "Id may not exist"}


@router.put("/{id}")
async def update_Tag_data(id: str, req: Tags = Body(...)):
    req = jsonable_encoder(req)
    req = {q: s for q,s in req.items() if len(str(s))!=0}
    updated_tag = await update_Tag(id, req)
    if updated_tag:
        return {"code": 200, "Data": "Data updated Successfully"}

    return {"code": 404, "Data": "Something Went Wrong"}
