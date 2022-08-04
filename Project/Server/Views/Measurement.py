from fastapi import APIRouter
from Server.Controller.User import retrieve_user_by_id

router = APIRouter()


@router.post("/BMI_CALCULATOR/{id}", response_description="BMI_CALCULATOR")
async def BMI_CALCULATOR(id: str):
    data = await retrieve_user_by_id(id)
    if data and  (data["Height"] != 0 and data["Weight"] != 0):
            height = data["Height"] / 100
            BMI = data["Weight"] / (height * height)
            return {"code": 200, "BMI": BMI}
    return {"code":404,"Data": "Something Went Wrong"}


# @router.post("/FAT_CALCULATOR/{id}", response_description="FAT_CALCULATOR")
# async def FAT_CALCULATOR(id:str):
#     data = await retrieve_user_by_id(id)
#     if data:
