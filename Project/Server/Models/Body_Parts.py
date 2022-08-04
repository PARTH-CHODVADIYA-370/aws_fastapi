from typing import List, Optional
from pydantic import BaseModel, HttpUrl


class Bodyparts(BaseModel):
    TITLE: str
    IMAGE: bytes

    class Config:
        schema_extra = {"example": {"TITLE": "Biceps", "IMAGE": "BASE64 PATH"}}
