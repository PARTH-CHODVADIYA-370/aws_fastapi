import base64
from logging import exception
from bson.objectid import ObjectId
from Server.Utils.Auth_Bearer import get_password_hash

from Server.Database import User_collection, Measurments_collection
import os

IMAGEDIR = os.getcwd()


def User_helper(data) -> dict:
    return {
        "_id": str(data["_id"]),
        "Name": str(data["Name"]),
        "Email": data["Email"],
        "Mobile": data["Mobile"],
        "Gender": data["Gender"],
        "Age": data["Age"],
        "Goal": data["Goal"],
        "Category": data["Category"],
        "Height": data["Height"],
        "Weight": data["Weight"],
        "Diets": data["Diets"],
        "Workout": data["Workout"],
        "Favourites_Recipes": data["Favourites_Recipes"],
        "Favourites_Exercises": data["Favourites_Exercises"],
        "Verified": data["Verified"],
        "IMAGE": data["IMAGE"],
        "Status": data["Status"],
        "Joining_Date": data["Joining_Date"],
    }


def Measurments_helper(data) -> dict:
    return {
        # "_id": str(data["_id"]),
        "User_id": str(data["User_id"]),
        "Traps1": data["Traps1"],
        "Traps": data["Traps"],
        "Neck": data["Neck"],
        "Chest": data["Chest"],
        "Shoulders": data["Shoulders"],
        "Forearms": data["Forearms"],
        "hip": data["hip"],
        "Abs": data["Abs"],
        "Glutes": data["Glutes"],
        "Lats": data["Lats"],
        "Hamstrings": data["Hamstrings"],
        "Quads": data["Quads"],
        "Waist_to_knee": data["Waist_to_knee"],
        "Waist": data["Waist"],
        "Biceps": data["Biceps"],
        "Biceps2": data["Biceps2"],
        "Ankle": data["Ankle"],
    }


async def Check_Email_Mobile(Data):
    try:
        Email = await User_collection.find_one({"Email": Data["Email"]})
        Phone_Number = await User_collection.find_one({"Mobile": Data["Mobile"]})
        if Email:
            return False
        elif Phone_Number:
            return False
        else:
            return True
    except:
        return True


async def Delete_Old_Image(id: str):
    image = await User_collection.find_one({"_id": ObjectId(id)})
    try:
        Del_Img = str(image["IMAGE"]).split("%2F")
        Path = (
            str(IMAGEDIR)
            + chr(92)
            + "Server"
            + chr(92)
            + "Static"
            + chr(92)
            + str(Del_Img[-1]).replace("/", chr(92))
        )
        os.remove(Path)
    except:
        return "Error Ocured"
    return Path


async def Add_User_Details(Data: dict) -> dict:

    user = await User_collection.insert_one(Data)
    # print(User_helper(user))
    if user:
        data = await User_collection.find_one({"Email": Data["Email"]})
        return User_helper(data)
    # return "User Successfully added"


async def add_user_measurments(data: dict):
    try:
        Measurments_collection.insert_one(data)
        return "Measures Successfully added"
    except Exception as e:
        return e


async def retrieve_all_Users():
    users = []
    async for data in User_collection.find():
        users.append(User_helper(data))
    return users


async def retrieve_user_measurment(id: str) -> dict:
    measurment = await Measurments_collection.find_one({"User_id": str(id)})
    if measurment:
        return Measurments_helper(measurment)


async def retrieve_user_by_id(user_id: str) -> dict:
    user = await User_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return User_helper(user)


async def delete_user_data(id: str):
    data = await User_collection.find_one({"_id": ObjectId(id)})
    if data:
        # Img_delete = await Delete_Old_Image(id)
        await User_collection.delete_one({"_id": ObjectId(id)})
        return "User Successfully deleted"
    return "User Not Found"


async def update_user(id: str, data: dict):
    if len(data) < 1:
        return False
    user = await User_collection.find_one({"_id": ObjectId(id)})
    # if flags == 1:
    #     data["IMAGE"]=user['IMAGE']
    if user:
        updated_user = await User_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_user:
            return True
        return False


# async def Image_Converter(Hax_Value):
#     random_name = str(uuid.uuid4())
#     decodeit = open(f"Server/static/{random_name}.jpg", 'wb')
#     decodeit.write(base64.b64decode(Hax_Value))
#     decodeit.close()
#     img_path = "http://localhost:8000/images?id=Server%2Fstatic%2F" + \
#         str(random_name)+".jpg"
#     return img_path
