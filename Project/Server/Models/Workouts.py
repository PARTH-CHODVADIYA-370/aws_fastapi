from typing import List
from pydantic import BaseModel, HttpUrl


class ImageSchema(BaseModel):
    url: HttpUrl
    name: str


class Workout(BaseModel):
    TITLE: str
    DESCRIPTION: str
    GOAL: str
    LEVEL: str
    BODYPART: List[str]
    EQUIPMENT: List[str]
    DURATION: str
    PRICE: str
    DAY_1: List[dict]
    DAY_2: List[dict]
    DAY_3: List[dict]
    DAY_4: List[dict]
    DAY_5: List[dict]
    DAY_6: List[dict]
    DAY_7: List[dict]
    STATUS: str
    IMAGE: bytes

    class Config:
        schema_extra = {
            "example": {
                "TITLE": "The 500-rep Challenge Routine",
                "DESCRIPTION": "When someone asks you to make a muscle, chances are you don’t flex your traps or rise onto your toes to show off your calves. You're going to roll up your sleeves and flex your biceps, inviting onlookers to your own personal gun show.",
                "GOAL": "Fast Loss",
                "LEVEL": "Elite",
                "BODYPART": [],
                "EQUIPMENT":[],
                "DURATION": "4 Days/Week",
                "PRICE": "Free",
                "DAY_1": ["FULL Plank"],
                "DAY_2": [],
                "DAY_3": [],
                "DAY_4": [],
                "DAY_5": [],
                "DAY_6": [],
                "DAY_7": [],
                "STATUS": "ACTIVE",
                "IMAGE": "BASE64 PATH",
            }
        }
