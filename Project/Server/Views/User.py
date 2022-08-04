from datetime import timedelta
from bson import ObjectId
from fastapi import APIRouter, Body, Depends
from Server.Utils.Auth_Bearer import JWTBearer, ACCESS_TOKEN_EXPIRE_MINUTES
from Server.Controller.Exercise import Exercise_helper
from Server.Controller.Workouts import workout_helper
from Server.Controller.User import User_helper
from Server.Database import Workout_collection
from Server.Utils.Image_Handler import Image_Converter
from Server.Utils.Auth_Bearer import (
    get_password_hash,
    create_access_token,
    verify_password,
)
from Server.Database import User_collection, Exercise_collection
from Server.Controller.User import update_user
from Server.Controller.User import (
    add_user_measurments,
    retrieve_user_measurment,
    Add_User_Details,
    Check_Email_Mobile,
    retrieve_all_Users,
    delete_user_data,
    retrieve_user_by_id,
)
from fastapi.encoders import jsonable_encoder
from Server.Models.User import user_details, add_masurment, Login, ChangePassword

router = APIRouter()


@router.post("/User_Registration", response_description="User Registration")
async def user_registration(data: user_details = Body(...)):
    data = jsonable_encoder(data)
    email = await Check_Email_Mobile(data)
    if email == False:
        return {"code": 200, "Msg": "Email or Mobile Already Registered"}
    if len(data["IMAGE"]) > 0:
        img_path = await Image_Converter(data["IMAGE"])
    else:
        img_path = ""
    data["IMAGE"] = str(img_path)
    data["PassWord"] = get_password_hash(data["PassWord"])
    output = await Add_User_Details(data)
    return {"code": 200, "User_id": output["_id"]}


@router.get("/Get_All_User", response_description="Get all User Details")
async def get_all_users():
    workout = await retrieve_all_Users()
    if workout:
        return {"code": 200, "Data": workout}
    return {"Data": workout, "Msg": "Empty list return"}


@router.get(
    "/Get_User_Data/{id}",
    response_description="Get user information data by id",
)
async def get_user_data(id):
    data = await retrieve_user_by_id(id)
    if data:
        return {"code": 200, "Data": data}
    return {"Msg": "Id may not exist"}


@router.delete("/Delete/{id}", response_description="Delete user data by id")
async def delete_user(id: str):
    data = await delete_user_data(id)
    if data:
        return {"code": 200, "Msg": data}
    return {"Msg": "Id may not exist"}


@router.put("/Update/{id}")
async def update_user_data(id: str, req: user_details):
    req = jsonable_encoder(req)
    data = {}
    for i, j in req.items():
        
        if (type(j) == str or type(j) == int) and (len(str(j)) > 0):
            data[i] = j

    if 'IMAGE' in data:
        if len(data["IMAGE"]) != 0:
            # Del_img= await Delete_Old_Image(id)
            imagepath = await Image_Converter(data["IMAGE"])
            data["IMAGE"] = imagepath

    updated_user = await update_user(id, data)
    if updated_user:
        return {"code": 200, "Data": "Data updated Successfully"}

    return {"code": 404, "Data": "Something Went Wrong"}


@router.post("/Status/{id}", response_description="Change Status")
async def change_status(id: str):
    data = await User_collection.find_one({"_id": ObjectId(id)})
    if data:
        if data["Status"] == "ACTIVE":
            await User_collection.update_one(
                {"_id": ObjectId(id)}, {"$set": {"Status": "Inactive"}}
            )
        else:
            await User_collection.update_one(
                {"_id": ObjectId(id)}, {"$set": {"Status": "ACTIVE"}}
            )
        return {"code": 200, "Msg": "Status Changed Successfully"}
    return {"code": 404, "Msg": "Id may not exist"}


@router.post("/Login/", response_description="Login User")
async def login(user: Login = Body(...)):
    user = jsonable_encoder(user)
    if user["Social"] == True:
        users = await User_collection.find_one({"Mobile": (user["Email"])})
    try:
        int(user["Email"])
        users = await User_collection.find_one({"Mobile": int(user["Email"])})
    except:
        users = await User_collection.find_one({"Email": user["Email"]})
        # mobiles = await user_collection.find_one({"mobile": user['email']})
    if users and user["Social"] == True:
        access_token = create_access_token(
            data={"sub": user["Email"]},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "_id": str(users["_id"]),
            "name": users["Name"],
        }
    if users:
        if verify_password(user["PassWords"], users["PassWord"]):
            access_token = create_access_token(
                data={"sub": users["Email"]},
                expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            )
            return {
                "code": 200,
                "access_token": access_token,
                "token_type": "bearer",
                "_id": str(users["_id"]),
                "name": users["Name"],
            }
        else:
            return {"code": 404, "message": "Password not match"}
    return {"code": 404, "message": "User not found or invalid Details"}


@router.post("/Change_Password/{id}", response_description="Change the password")
async def change_password(id: str, user: ChangePassword = Body(...)):
    user = jsonable_encoder(user)
    data = await User_collection.find_one({"_id": ObjectId(id)})
    print(user["old_passWords"])
    if verify_password(user["old_passWords"], data["PassWord"]):
        data["PassWord"] = get_password_hash(user["new_password"])
        await User_collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": data})
        return {"code": 200, "message": "Password changed successfully"}
    else:
        return {"code": 404, "message": "Please enter Valid Old Password"}


@router.post("/Add_Measurment/{id}", response_description="Add Measurment")
async def add_measurment(id: str, measurment: add_masurment = Body(...)):
    data = jsonable_encoder(measurment)
    data["User_id"] = str(id)
    status = await add_user_measurments(data)
    return {"code": 200, "message": status}


@router.get("/Get_Measurment/{id}", response_description="Get Measurment")
async def get_measurment(id: str):
    data = await retrieve_user_measurment(id)
    if data:
        return {"code": 200, "Data": data}
    return {"Msg": "Id may not exist"}


@router.get("/Get_User_Workout/{id}", response_description="Get user workout")
async def get_user_workout(id: str):
    user = await User_collection.find_one({"_id": ObjectId(id)})
    user = User_helper(user)
    if user:
        workout_list = user["Workout"]
        output = []
        for each_workout in workout_list:
            workout = await Workout_collection.find_one({"_id": ObjectId(each_workout)})
            workout = workout_helper(workout)
            output.append(workout)
        return {"code": 200, "Data": output}
    else:
        return {"code": 404, "Data": "User not found"}


@router.get("/User_Exercise/{id}", response_description="Get user Exercise Details")
async def get_user_exercise_details(id):
    try:
        user = await User_collection.find_one({"_id": ObjectId(id)})
        user = User_helper(user)
        if user is not None:
            workout_list = user["Workout"]
            output = []
            for each_workout in workout_list:
                if len(each_workout) > 0:
                    workout = await Workout_collection.find_one(
                        {"_id": ObjectId(each_workout)}
                    )
                    workout = workout_helper(workout)
                    if workout is not None:
                        for day in range(1, 8):
                            DAY = "DAY_" + str(day)
                            if len(workout[DAY]) > 0:
                                for excrcise_id in workout[DAY]:
                                    if len(excrcise_id) > 1:
                                        exercise = await Exercise_collection.find_one(
                                            {"_id": ObjectId(excrcise_id)}
                                        )
                                        output.append(Exercise_helper(exercise))
            if len(output) == 0:
                return {
                    "code": 200,
                    "msg": "Not any workout assigned contact administration",
                }
            return {"code": 200, "msg": output}
        else:
            return {"code": 400, "msg": "user not found"}
    except Exception as e:
        return {"code": 404, "Data": "Something Went Wrong", "msg": e.args}
