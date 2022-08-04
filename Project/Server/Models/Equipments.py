from typing import List, Optional
from pydantic import BaseModel, HttpUrl


class Equipments(BaseModel):
    TITLE: str
    IMAGE: bytes
    # IMAGE:  Optional[ImageSchema] = None

    class Config:
        schema_extra = {"example": {"TITLE": "Dumbels", "IMAGE": "BASE64 PATH"}}
