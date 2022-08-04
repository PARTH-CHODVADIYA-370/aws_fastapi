import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from Server.Views.Tags import router as Tag
from Server.Views.Post import router as Post
from Server.Views.User import router as User
from Server.Views.Goals import router as Goals
from Server.Views.Recipe import router as Recipe
from Server.Views.Levels import router as Levels
from Server.Views.Workouts import router as Workout
from Server.Views.Exercise import router as Exercise
from Server.Views.Categories import router as Category
from Server.Views.Body_parts import router as Bodyparts
from Server.Views.Equipments import router as Equipments
from Server.Views.Subscription import router as Subscription
from Server.Utils.Payment import router as Razorpay
from Server.Views.Measurement import router as Measurement
from Server.Views.FoodCal import router as FoodCal
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.mount("/Static", StaticFiles(directory="Server"), name="Static")

IMAGEDIR = os.getcwd()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(FoodCal, tags=["FoodCal"], prefix="/FoodCal")
app.include_router(Workout, tags=["Workout"], prefix="/Workout")
app.include_router(User, tags=["User"], prefix="/User")
app.include_router(Exercise, tags=["Exercise"], prefix="/Exercises")
app.include_router(Bodyparts, tags=["Bodyparts"], prefix="/Bodyparts")
app.include_router(Recipe, tags=["Recipe"], prefix="/Recipe")
app.include_router(Equipments, tags=["Equipments"], prefix="/Equipments")
app.include_router(Category, tags=["Categories"], prefix="/Categories")
app.include_router(Tag, tags=["Tags"], prefix="/Tags")
app.include_router(Levels, tags=["Levels"], prefix="/Levels")
app.include_router(Goals, tags=["Goals"], prefix="/Goals")
app.include_router(Post, tags=["Post"], prefix="/Post")
app.include_router(Subscription, tags=["Subscription"], prefix="/Subscription")
app.include_router(Razorpay, tags=["Razorpay"], prefix="/Payments")
app.include_router(Measurement, tags=["Measurement"], prefix="/Measurement")


@app.get("/images", tags=["IMAGE"])
def get_images(id):
    random_index = id
    path = f"{IMAGEDIR}/{random_index}"
    return FileResponse(path)


@app.get("/", tags=["APP"])
def read_root():
    return {"message": "Welcome to this fantastic app!"}
