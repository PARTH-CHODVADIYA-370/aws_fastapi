from typing import List, Optional
from pydantic import BaseModel, HttpUrl


class Categories(BaseModel):
    TITLE: str
    IMAGE: bytes
    # IMAGE:  Optional[ImageSchema] = None
    class Config:
        schema_extra = {"example": {"TITLE": "Salads", "IMAGE": "BASE64 PATH"}}
