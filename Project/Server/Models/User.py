from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class user_details(BaseModel):
    Name: str
    Email: str
    PassWord: str
    Mobile: int
    Gender: str
    Age: int
    Goal: str
    Category: str
    Height: int
    Weight: int
    Verified: str
    Diets: List[str]
    Workout: List[str]
    Favourites_Exercises: List[str]
    Favourites_Recipes: List[str]
    Status: str
    Joining_Date: Optional[datetime] = Field(default_factory=datetime.utcnow)
    Last_Login: Optional[datetime] = Field(default_factory=datetime.utcnow)
    IMAGE: bytes

    class Config:
        schema_extra = {
            "example": {
                "Name": "kavibhai",
                "Email": "kavi@example.com",
                "PassWord": "1234",
                "Mobile": 9908092111,
                "Gender": "Male",
                "Age": 25,
                "Goal": "Gain",
                "Category": "Veg",
                "Height": 4.6,
                "Weight": 55,
                "Verified": "Yes",
                "Diets": [],
                "Workout": [],
                "Favourites_Exercises": [],
                "Favourites_Recipes": [],
                "Status": "ACTIVE",
                "IMAGE": "BASE64 PATH",
            }
        }


class Login(BaseModel):
    Email: str
    PassWords: str
    Social: Optional[bool]

    class Config:
        schema_extra = {
            "example": {
                "Email": "parth@gmail.com",
                "Social": False,
                "PassWords": "1234",
            }
        }


class ChangePassword(BaseModel):
    old_passWords: str
    new_password: str

    class Config:
        schema_extra = {"example": {"old_passWords": "1234", "new_password": "123456"}}


class add_masurment(BaseModel):
    Traps1: str
    Traps: str
    Neck: str
    Chest: str
    Shoulders: str
    Forearms: str
    hip: str
    Abs: str
    Glutes: str
    Lats: str
    Hamstrings: str
    Quads: str
    Waisttoknee: str
    Waist: str
    Biceps: str
    Biceps2: str
    Ankle: str

    class Config:
        schema_extra = {
            "example": {
                "Traps1": "1",
                "Traps": "2",
                "Neck": "3",
                "Chest": "4",
                "Shoulders": "6",
                "Forearms": "7",
                "hip": "8",
                "Abs": "9",
                "Glutes": "10",
                "Lats": "11",
                "Hamstrings": "12",
                "Quads": "13",
                "Waist_to_knee": "14",
                "Waist": "15",
                "Biceps": "16",
                "Biceps2": "17",
                "Ankle": "18",
            }
        }
