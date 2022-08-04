

from Server.Database import User_collection, Workout_collection
from Server.Database import Exercise_collection
import os
from bson.objectid import ObjectId

IMAGEDIR = os.getcwd()


def Exercise_helper(data) -> dict:
    return {
        "_id": str(data["_id"]),
        "TITLE": str(data["TITLE"]),
        "BODYPART": data["BODYPART"],
        "EQUIPMENT": data["EQUIPMENT"],
        "LEVEL": data["LEVEL"],
        "REST": data["REST"],
        "SETS": data["SETS"],
        "REPS": data["REPS"],
        "VIDEO_URL": data["VIDEO_URL"],
        "INSTRUCTION": data["INSTRUCTION"],
        "TIPS": data["TIPS"],
        "IMAGE": data["IMAGE"],
    }


async def Check_Exercises(schema: dict):
    try:
        title = await Exercise_collection.find_one({"TITLE": schema["TITLE"]})
        if title:
            return False
        else:
            return True
    except:
        return True


async def Delete_Old_Image(id: str):
    image = await Exercise_collection.find_one({"_id": ObjectId(id)})
    try:
        del_img = str(image["IMAGE"]).split("%2F")
        path = (
            str(IMAGEDIR)
            + chr(92)
            + "Server"
            + chr(92)
            + "Static"
            + chr(92)
            + str(del_img[-1]).replace("/", chr(92))
        )
        os.remove(path)
    except:
        return "Error Ocured"
    return path


async def Add_Exercise(schema: dict) -> dict:

    await Exercise_collection.insert_one(schema)
    return "Exercise Successfully added"


async def retrieve_all_Exercises():
    exercise = []
    async for data in Exercise_collection.find():
        exercise.append(Exercise_helper(data))
    return exercise


async def retrieve_exercise_by_id(exercise_id: str) -> dict:
    exercise = await Exercise_collection.find_one({"_id": ObjectId(exercise_id)})
    if exercise:
        return Exercise_helper(exercise)
    else:
        return "No Exercise found by this id"

async def add_data(id:str, data):
    await User_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": {"Favourites_Exercises" : data}}
        )

async def update_workout(id: str, data:dict):
    await Workout_collection.update_one({"_id": ObjectId(id)},{"$set": data})

async def delete_exercise_data(id: str):
    data = await Exercise_collection.find_one({"_id": ObjectId(id)})
    if data:
        async for user in User_collection.find():
            user_id=  str(user["_id"])
            user_exercise =user['Favourites_Exercises']

            if id in user_exercise:
                    user_exercise.remove(id)
                    await add_data(user_id,user_exercise)
        
        async for workout in Workout_collection.find():
                workout_id =str(workout["_id"])
                day_1 =workout["DAY_1"]
                day_2 =workout["DAY_2"]
                day_3 =workout["DAY_3"]
                day_4 =workout["DAY_4"]
                day_5 =workout["DAY_5"]
                day_6 =workout["DAY_6"]
                day_7 =workout["DAY_7"]
                if  id in day_1:
                    day_1.remove(id)
                elif id in day_2:
                    day_2.remove(id)
                elif id in day_3:
                    day_3.remove(id)
                elif id in day_4:
                    day_4.remove(id)
                elif id in day_5:
                    day_5.remove(id)
                elif id in day_6:
                    day_6.remove(id)
                elif id in day_7:
                    day_7.remove(id)
                workout_data= {"DAY_1": day_1,"DAY_2": day_2,"DAY_3": day_3,"DAY_4": day_4,"DAY_5": day_5,"DAY_6": day_6,"DAY_7": day_7}
                await update_workout(workout_id,workout_data)
        # Img_delete = await Delete_Old_Image(id)
        await Exercise_collection.delete_one({"_id": ObjectId(id)})
        return "Data Successfully deleted"
    return "Data Not Found"


async def update_exercise(id: str, data: dict):
    if len(data) < 1:
        return False
    exercise = await Exercise_collection.find_one({"_id": ObjectId(id)})
    if exercise:
        updated_exercise = await Exercise_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_exercise:
            return True
        return False
