from dis import Instruction
from typing import List, Optional
from pydantic import BaseModel, HttpUrl


class Exercise(BaseModel):
    TITLE: str
    BODYPART: List[str]
    EQUIPMENT: List[str]
    LEVEL: str
    REST: str
    SETS: str
    REPS: str
    VIDEO_URL: str
    INSTRUCTION: str
    TIPS: str
    IMAGE: bytes
    # IMAGE:  Optional[ImageSchema] = None

    class Config:
        schema_extra = {
            "example": {
                "TITLE": "Reclining Triceps Press",
                "BODYPART": [],
                "EQUIPMENT": [],
                "LEVEL": "Beginner",
                "REST": "45 Sec",
                "SETS": "4",
                "REPS": "15",
                "VIDEO_URL": "None",
                "INSTRUCTION": "Draw your abs in, rolling the bar back to your knees. That's 1 rep; do 10.",
                "TIPS": "Drink Water",
                "IMAGE": "BASE64 PATH",
            }
        }
