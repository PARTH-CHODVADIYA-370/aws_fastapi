from pydantic import BaseModel, HttpUrl


class Goals(BaseModel):
    TITLE: str
    DESCRIPTION: str
    IMAGE: bytes
    # IMAGE:  Optional[ImageSchema] = None

    class Config:
        schema_extra = {
            "example": {
                "TITLE": "Lose Weight",
                "DESCRIPTION": "Lose weight by 10 kg",
                "IMAGE": "BASE64 PATH",
            }
        }
