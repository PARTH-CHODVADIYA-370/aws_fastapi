from pydantic import BaseModel, HttpUrl


class Levels(BaseModel):
    TITLE: str
    RATE: str
    IMAGE: bytes
    # IMAGE:  Optional[ImageSchema] = None

    class Config:
        schema_extra = {
            "example": {"TITLE": "Elite", "RATE": "4", "IMAGE": "BASE64 PATH"}
        }
